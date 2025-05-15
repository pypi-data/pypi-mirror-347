from azure.identity import DefaultAzureCredential, CertificateCredential
from azure.keyvault.secrets import SecretClient
from azure.keyvault.secrets import SecretClient
import base64
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates

class AuthHelper:
    def __init__(self, keyvault_url: str, env: str):
        '''
        Initialises an AuthHelper object using a URL for an Azure Key Vault,
        which creates a SecretClient for further secret retrieval.

        The runtime entity must have permissions for the Key Vault, whether 
        they are a user, application etc. For a user this is best managed via
        Azure CLI login, and Function Apps (where this is intended to be 
        used), should have a managed identity for the Key Vault.
        '''
        self.keyvault_url = keyvault_url
        self.env = env

        # Create credential using default method
        self.credential = DefaultAzureCredential(exclude_environment_credential=True)

        # Create secret client for accessing key vault
        self.secret_client = SecretClient(
            vault_url=self.keyvault_url,
            credential=self.credential
        )

    def get_secret(self, secret_name: str) -> str:
        """
        Retrieves a secret value from Azure Key Vault using SecretClient.

        Params:
            secret_name: The name of the secret in Key Vault.

        Returns:
            The secret value as a string.
        """
        secret = self.secret_client.get_secret(secret_name)
        return secret.value

    def authenticate_as_principal_cert(self) -> CertificateCredential:
        """
        Authenticates with Azure services in the appropriate environment using
        the retrieved certificate and other details.

        Returns:
            A CertificateCredential object.
        """
        # Retrieve the certificate
        self.client_id = self.get_secret('service-principal-client-id')
        self.tenant_id = self.get_secret('tenant-id')
        pfx_base64 = self.get_secret(f'DataFactoryPrincipal-{self.env}-Cert')
        #pfx_base64 = secret.value
        pfx_bytes = base64.b64decode(pfx_base64)

        # Load PKCS#12 certificate
        pfx_password = None
        private_key, certificate, additional_certificates = load_key_and_certificates(
            data=pfx_bytes,
            password=pfx_password
        )

        # Serialise to PEM format
        pem_private_key = private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption()
        )
        pem_certificate = certificate.public_bytes(encoding=Encoding.PEM)

        # Add private key data to public key data
        pem_data = pem_private_key + pem_certificate

        for cert in additional_certificates or []:
            pem_data += cert.public_bytes(encoding=Encoding.PEM)

        # Create and return the CertificateCredential
        return CertificateCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            certificate_data=pem_data
        )