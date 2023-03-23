import os
import json
import azure.functions as func
from azure.cosmos import CosmosClient

def main(req: func.HttpRequest):
    
    DATABASE_URL = os.environ['database_url']
    DATABASE_KEY = os.environ['database_key']
    DATABASE_NAME = os.environ['database_name']
    DATABASE_CONTAINER_NAME = os.environ['database_container_name']
    MAP_URL = os.environ['MAP_URL']

    cosmos_client = CosmosClient(DATABASE_URL, credential=DATABASE_KEY)
    database = cosmos_client.get_database_client(DATABASE_NAME)
    database_container = database.get_container_client(DATABASE_CONTAINER_NAME)

    query = 'SELECT * from c'
    items = list(database_container.query_items(query, enable_cross_partition_query=True))

    headers = {
        'Access-Control-Allow-Origin': MAP_URL,
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }

    return func.HttpResponse(json.dumps(items), headers=headers, status_code=200)