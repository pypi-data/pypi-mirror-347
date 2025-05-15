import urllib.parse
import sqlalchemy as sa
from .azure_auth import AuthHelper
import struct

class AzureSQLHelper:
    """
    A context manager that creates a SQLAlchemy Engine with token 
    authentication acquired via Service Principal for Azure SQL.
    """

    def __init__(self, auth_helper: AuthHelper, access_token: str):
        self.server = auth_helper.get_secret("dwh-server")
        self.database = auth_helper.get_secret("dwh-db")

        #SQL token
        self.access_token = access_token
        
        odbc_params = (
            "Driver={ODBC Driver 18 for SQL Server};"
            f"Server={self.server};"
            f"Database={self.database};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
        )

        # Expand token per docs (this took me bloody days to figure out lol)
        #https://learn.microsoft.com/en-us/sql/connect/odbc/using-azure-active-directory?view=azuresqldb-current#authenticating-with-an-access-token
        #https://learn.microsoft.com/en-us/python/api/adal/adal.authentication_context.AuthenticationContext?view=azure-python#methods
        #https://stackoverflow.com/questions/61069715/pyodbc-will-support-connecting-to-an-azure-sql-db-using-the-ad-access-token-inst

        '''
        For each byte in the access token, append <byte> + "\0x00"
        then prepend 4-byte int to indicate total length, since this is what
        the odbc driver is expecting to see when passing sql_copt_ss_access_token
        '''

        self.expanded_token = b''

        for i in bytes(self.access_token, "UTF-8"):
            self.expanded_token += bytes({i})
            self.expanded_token += bytes(1)
        
        self.token_struct = struct.pack("=i", len(self.expanded_token)) + self.expanded_token
        
        encoded_params = urllib.parse.quote_plus(odbc_params)

        # SQLAlchemy URI
        self.db_uri = f"mssql+pyodbc:///?odbc_connect={encoded_params}"
        self._engine = None

    def __enter__(self):
        """
        Create and return the SQLAlchemy Engine.
        """
        self._engine = sa.create_engine(
            self.db_uri,
            connect_args={'attrs_before': {
                    1256: self.token_struct
                }
            }
        )
        return self._engine

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Dispose of the SQLAlchemy engine (closing any open connections).
        """
        if self._engine:
            self._engine.dispose()
            self._engine = None