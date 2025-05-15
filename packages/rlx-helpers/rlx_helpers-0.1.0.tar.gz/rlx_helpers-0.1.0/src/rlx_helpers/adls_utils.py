from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
import logging


class ADLSHelper:
    def __init__(self, account_url: str):
        """
        Initialises the ADLSHelper by creating a DataLakeServiceClient using DefaultAzureCredential.

        Params:
            account_url: The full ADLS Gen2 endpoint ie 'https://<storage_account_name>.dfs.core.windows.net'
        """
        self.account_url = account_url
        self.logger = logging.getLogger(self.__class__.__name__)

        try:
            # Initialise DefaultAzureCredential
            self.credential = DefaultAzureCredential()
            self.logger.info("Successfully initialised DefaultAzureCredential.")

            # Create DataLakeServiceClient
            self.service_client = DataLakeServiceClient(
                account_url=self.account_url,
                credential=self.credential
            )
            self.logger.info(f"Connected to ADLS account: {self.account_url}")
        except Exception as e:
            self.logger.error(f"Failed to initialise ADLSHelper: {e}")
            raise

    def get_file_system_client(self, file_system_name: str):
        """
        Retrieves a FileSystemClient for the specified file system.

        Params:
            file_system_name: The name of the file system (container) in ADLS.

        Returns:
            A FileSystemClient instance.
        """
        try:
            return self.service_client.get_file_system_client(file_system_name)
        except Exception as e:
            self.logger.error(f"Failed to get FileSystemClient for '{file_system_name}': {e}")
            raise

    def read_file(self, file_system_name: str, file_path: str) -> bytes:
        """
        Reads a file's content from ADLS Gen2.

        Params:
            file_system_name: The name of the file system (container).
            file_path: The path to the file within the file system.

        Returns:
            The file contents as bytes.
        """
        try:
            file_system_client = self.get_file_system_client(file_system_name)
            file_client = file_system_client.get_file_client(file_path)

            download = file_client.download_file()
            file_contents = download.readall()
            self.logger.info(f"Successfully read file: {file_path} in {file_system_name}")
            return file_contents
        except ResourceNotFoundError:
            self.logger.error(f"The file {file_path} was not found in {file_system_name}.")
            raise
        except HttpResponseError as e:
            self.logger.error(f"HTTP error occurred while reading {file_path}: {e.message}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while reading {file_path}: {e}")
            raise

    def write_file(self, file_system_name: str, file_path: str, data: bytes) -> None:
        """
        Writes data to a file in ADLS Gen2.

        Params:
            file_system_name: The name of the file system (container).
            file_path: The path to the file within the file system.
            data: The content to be written, as bytes.

        Returns:
            None
        """
        try:
            file_system_client = self.get_file_system_client(file_system_name)
            file_client = file_system_client.get_file_client(file_path)

            # Create or overwrite the file
            file_client.create_file()
            self.logger.info(f"Created file: {file_path} in {file_system_name}")

            # Upload content
            file_client.upload_data(data, overwrite=True)
            self.logger.info(f"Successfully wrote to file: {file_path} in {file_system_name}")
        except HttpResponseError as e:
            self.logger.error(f"HTTP error occurred while writing {file_path}: {e.message}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while writing {file_path}: {e}")
            raise

    def list_files(self, file_system_name: str, directory_path: str = ""):
        """
        Lists all files in a specified directory within a file system.

        Params:
            file_system_name: The name of the file system (container).
            directory_path: The path to the directory within the file system.

        Returns:
            A list of file paths.
        """
        try:
            file_system_client = self.get_file_system_client(file_system_name)
            paths = file_system_client.get_paths(path=directory_path)
            files = [path.name for path in paths if not path.is_directory]
            self.logger.info(f"Listed {len(files)} files in '{directory_path}' of '{file_system_name}'.")
            return files
        except HttpResponseError as e:
            self.logger.error(f"HTTP error occurred while listing files in '{directory_path}': {e.message}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while listing files in '{directory_path}': {e}")
            raise
