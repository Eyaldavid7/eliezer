from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from google.cloud import storage
from PyPDF2 import PdfReader
from googletrans import Translator
import os
import requests
import uuid
import arabic_reshaper
import io
import Gptebnedding
import bidi
import re




def Embooks():
    
    # Create the azure translation client
    subscription_key = 'e264be75492e4e998f195bbf6b1b3006'
    endpoint = 'https://api.cognitive.microsofttranslator.com/'
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credentials=credentials)

    # Create the google storage client
    storage_client = storage.Client()
    bucket_name = 'bookembdding'
    bucket = storage_client.bucket(bucket_name)

    # Define regex pattern to split text into sentences
    sentence_pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    00
    # Get the blob containing the PDF file
    blob_name = 'prism_8-4_31-39_Finkel.pdf'
    blob = bucket.blob(blob_name)

    # Download the PDF file to memory
    pdf_bytes = blob.download_as_bytes()

    # Open the pdf file
    pdf_file = io.BytesIO(pdf_bytes)
    pdf_file = PdfReader(pdf_file)

    # Insert all the pages into one tex string
    text = ''
    for page in range(len(pdf_file.pages)):
        extracted_text  =    pdf_file.pages[page].extract_text()
        text += extracted_text

    # Split text into groups of 5 sentences
    sentences = sentence_pattern.split(text)
    group_size = 10
    groups = [sentences[i:i+group_size] for i in range(0, len(sentences), group_size)]

    # Saveing each pargrph after translation to the blob    
    for i, group in enumerate(groups):
        text = " ".join(group)
        text = text.replace('\n', ' ')
        translated_text = Gptebnedding.InsertEmbdings2(text)


