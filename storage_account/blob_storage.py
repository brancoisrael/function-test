from azure.storage.blob import BlobServiceClient, ContentSettings, __version__
from azure.core import exceptions
from os import getenv, path, remove
from utils.local_file import write_file
import logging
import tempfile

BUCKET_NAME = getenv("BUCKET_NAME")
AZURE_ACCOUNT_NAME = getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = getenv('AZURE_ACCOUNT_KEY')

class BlobStorage():
    
    def __init__(self) -> None:
        try:
            logging.info("Azure Blob Storage v" + __version__)
            connection_string = f'DefaultEndpointsProtocol=https;AccountName={AZURE_ACCOUNT_NAME};AccountKey={AZURE_ACCOUNT_KEY};EndpointSuffix=core.windows.net'
            self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            self.container_client = self.blob_service_client.create_container(name=BUCKET_NAME,public_access='blob')

        except exceptions.ResourceExistsError as ex:
            logging.info(f"Container '{BUCKET_NAME}' already exists")

        except Exception as ex:
            logging.error(ex)

    def save_file(self, file)->str:
        file_name = write_file(file)
        file_path = path.join(tempfile.gettempdir(), file_name)
        temp_file = open(file_path, mode='rb')
        self.upload_blob(temp_file, file_name,file.content_type)
        temp_file.close()
        remove(file_path)
        return file_name
       
    def upload_blob(
        self,
        source_file_name,
        destination_blob_name: str,
        blob_type: str,
    ):
        blob_client = self.blob_service_client.get_blob_client(
            container=BUCKET_NAME, blob=destination_blob_name)

        # Upload the created file
        content_settings = ContentSettings(content_type=blob_type)
        blob_client.upload_blob(
            source_file_name, content_settings=content_settings)

        logging.info(
            "File {} uploaded to container {}: {}".format(
                source_file_name, BUCKET_NAME, destination_blob_name
            )
        )

    def delete_blob(self, blob_name: str):
        blob_name = blob_name.replace(
            self.get_url_prefix(), ""
        )

        blob_client = self.blob_service_client.get_blob_client(
            container=BUCKET_NAME, blob=blob_name)

        blob_client.delete_blob()

        logging.info("Blob {} deleted.".format(blob_name))

    def get_url_prefix(self) -> str:
        return (
            f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{BUCKET_NAME}/"
        )
           
blob_storage = BlobStorage()