import dbaccess
import pandas as pd
from google.cloud import storage


class GoogleBucketDbAccess():
  def __init__(self):
    self.LOCAL_FILENAME = 'local_db.pdf'
    self.storage_client = storage.Client()
    self.bucket = self.storage_client.bucket('tals-openai-bucket')
    self.blob = self.bucket.blob('embding.pdf')

  def get(self):
    """
    This function fetches a pdf file that contains saved embeddings from a Google Cloud blob
    and saves it on the local db.
    """
    self.blob.download_to_filename(self.LOCAL_FILENAME)
  
  def save(self):
    """
    This function saves the local pdf db specified by LOCAL_FILENAME to the Google Cloud blob
    """
    self.blob.upload_from_filename(self.LOCAL_FILENAME)
 
  def ensureExists(self):
    """
    This function ensures that the remote db exists in the google cloud blob.
    If not, the function creates it.
    """
    if self.blob.exists():
        print("Blob already exists.")
        return

    local_db = open(self.LOCAL_FILENAME, "w")
    local_db.close()
    self.blob.upload_from_filename(self.LOCAL_FILENAME)

  def read_blob(self, blob_name, local_file_name):
    """
    This function fetches a pdf file that contains extra data for the embedding from a Google Cloud blob 
    and saves it on a local file.
    """
    blob = self.bucket.blob(blob_name)
    blob.download_to_filename(local_file_name)
