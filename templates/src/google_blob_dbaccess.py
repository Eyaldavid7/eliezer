import dbaccess
import pandas as pd
from google.cloud import storage

class GoogleBucketDbAccess():
  def __init__(self):
    self.LOCAL_FILENAME = 'tmp_database.csv'

  def get(self):
    # Create the google storage client
    storage_client = storage.Client()
    bucket_name = 'bookembdding'
    bucket = storage_client.bucket(bucket_name)

    # Get the blob containing the PDF file
    blob_name = 'Embding3.csv'
    blob = bucket.blob(blob_name)

    blob.download_to_filename(self.LOCAL_FILENAME)
    df = pd.read_csv(self.LOCAL_FILENAME)
    return df
  def ensureExists(self):
    # Create the google storage client
    storage_client = storage.Client()
    bucket_name = 'bookembdding'
    bucket = storage_client.bucket(bucket_name)

    #Create the dataframe with columns for time and message
    df = pd.DataFrame(columns=["time","message", "ada_search"])
    # Save the dataframe to a csv file
    df.to_csv(self.LOCALFILENAME,index=False)
    # Upload the created file
    with open(file=self.LOCALFILENAME, mode="rb") as data:
        blob = bucket.blob()
        blob.upload_blob(data)    
  def save(self, df):
    df.to_csv(self.LOCAL_FILENAME, index=False)
       # Create the google storage client
    storage_client = storage.Client()
    bucket_name = 'bookembdding'
    bucket = storage_client.bucket(bucket_name)

    # Get the blob containing the PDF file
    blob_name = 'Embding3.csv'
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(self.LOCAL_FILENAME)

  def ensureExists(self):
    # Create the google storage client
    storage_client = storage.Client()
    bucket_name = 'bookembdding'
    bucket = storage_client.bucket(bucket_name)

    # Get the blob containing the PDF file
    blob_name = 'Embding3.csv'
    blob = bucket.blob(blob_name)

    if blob.exists():
        print("Blob already exists.")
        return

    # Create the dataframe with columns for time and message
    df = pd.DataFrame(columns=["time","message", "ada_search"])
    # Save the dataframe to a csv file
    df.to_csv(self.LOCAL_FILENAME, index=False)
    # Upload the created file
    blob.upload_from_filename(self.LOCAL_FILENAME)