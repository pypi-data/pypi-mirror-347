from .azure_auth import AuthHelper
import time

class ServicePrincipal:
    def __init__(self, auth_helper: AuthHelper):
        """
        Initialises a ServicePrincipal object by fetching necessary secrets, creating
        a CertificateCredential, and initialising token settings.

        Params:
            key_vault_url: The URL of the Azure Key Vault.
        """

        # Create CertificateCredential
        self.app_credential = auth_helper.authenticate_as_principal_cert()
        #self.app_credential = auth_helper.authenticate_as_principal_secret()

        # Token caching
        self._graph_token = None
        self._graph_token_expiry = 0
        self._sql_token = None
        self._sql_token_expiry = 0

    def get_graph_token(self) -> str:
        """
        Uses the Service Principal's API permissions to obtain and cache an
        access token for the Microsoft Graph API.

        Returns:
            An access token as a string.
        """
        if not self._graph_token or time.time() >= self._graph_token_expiry:
            # Fetch a new token if none exists or the current one is expired
            graph_scope = "https://graph.microsoft.com/.default"
            token_response = self.app_credential.get_token(graph_scope)
            self._graph_token = token_response.token
            self._graph_token_expiry = time.time() + token_response.expires_on - 60  # Refresh 1 min early
        return self._graph_token
    
    def get_sql_server_token(self) -> str:
        '''
        Uses the Service Principal's API permissions to obtain and cache an
        access token for Azure SQL database resources.

        Returns:
            An access token as a string.
        '''
        if not self._sql_token or time.time() >= self._sql_token_expiry:
            sql_scope = "https://database.windows.net/.default"
            token_response = self.app_credential.get_token(sql_scope)
            self._sql_token = token_response.token
            self._sql_token_expiry = time.time() + token_response.expires_on - 60
            return self._sql_token