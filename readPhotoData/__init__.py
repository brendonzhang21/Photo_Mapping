import os
import io
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

from azure.storage.blob import BlobClient
from azure.cosmos import CosmosClient
import azure.functions as func

def ConvertDMStoDD(DMS_value):
    degree = DMS_value[0] + DMS_value[1]/60.0 + DMS_value[2]/3600.0
    return degree

def main(myblob: func.InputStream):

    CONNECTION_STRING = os.environ['AzureWebJobsStorage']
    STORAGE_CONTAINER_NAME = os.environ['storage_container_name']
    DATABASE_URL = os.environ['database_url']
    DATABASE_KEY = os.environ['database_key']
    DATABASE_NAME = os.environ['database_name']
    DATABASE_CONTAINER_NAME = os.environ['database_container_name']

    cosmos_client = CosmosClient(DATABASE_URL, credential=DATABASE_KEY)
    database = cosmos_client.get_database_client(DATABASE_NAME)
    database_container = database.get_container_client(DATABASE_CONTAINER_NAME)

    blobname = myblob.name.split('/', 1)[1]
    blob = BlobClient.from_connection_string(conn_str=CONNECTION_STRING, container_name=STORAGE_CONTAINER_NAME, blob_name=blobname)
    blob_data = blob.download_blob().readall()

    image = Image.open(io.BytesIO(blob_data))
    exif_data = image._getexif()
    gps_tag = False
    gps_data = {}
    if exif_data:
        for tag, value in exif_data.items():
            current_tag = TAGS.get(tag)
            if current_tag == "GPSInfo":
                gps_tag = True
                for t in value:
                    gps_info = GPSTAGS.get(t)
                    gps_data[gps_info] = value[t]

    if gps_tag:

        latitude = ConvertDMStoDD(gps_data["GPSLatitude"])
        if gps_data["GPSLatitudeRef"] == "S":
            latitude *= -1

        longitude = ConvertDMStoDD(gps_data["GPSLongitude"])
        if gps_data["GPSLongitudeRef"] == "W":
            longitude *= -1

        database_container.upsert_item({
            'id': blobname,
            'filename': blobname,
            'GPS_Lat': str(latitude),
            'GPS_Long': str(longitude)
        })
        



