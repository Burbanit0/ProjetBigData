import pandas as pd
from pymongo import MongoClient
import json
import boto3
import os

BUCKET_NAME = 'bigdatabucket115585644'
OBJECT_NAME = 'data.csv'
path = "./"
DB_NAME = 'resultDB'


def download_file(bucket_name, object_name, path):

    s3_client = boto3.client('s3')

    s3_client.download_file(bucket_name, object_name, path)
    print('download success')


def mongoimport(csv_path, db_name, db_url='localhost', db_port=27017):

    client = MongoClient(db_url, db_port)
    df = pd.read_csv(csv_path)
    data = df.to_dict(orient="records")
    db = client[db_name]
    print(db)
    collection_name = input("Collection name : ")
    db.create_collection(collection_name).insert_many(data)


def main():

    bucket_name = input("S3 Bucket Name : ")
    object_name = input("Filename : ")
    # path = input("Set a local path (File will be remove from this path): ")
    db_name = input("Name of the database : ")
    try:
        download_file(bucket_name, object_name, path + object_name)
        mongoimport(path + object_name, db_name)
        os.remove(path + object_name)
    except:
        print("Import failed")


if __name__ == '__main__':
    main()