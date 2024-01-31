import logging

import boto3
from botocore.exceptions import ClientError

from app.configs.config import S3Settings

s3Settings = S3Settings()
session = boto3.session.Session()

s3_client = session.client(service_name="s3", aws_access_key_id=s3Settings.S3_ACCESS_KEY,
                           aws_secret_access_key=s3Settings.S3_SECRET_KEY,
                           endpoint_url=s3Settings.S3_ENDPOINT
                           )


async def s3_upload_image(file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param s3_client:
    :param file_name: File to upload
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Если не было задано имя для файла, то поставь его название
    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_file(file_name, s3Settings.S3_BUCKET_NAME, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


async def s3_create_download_link(file_name: str):
    # https://bucket_name.endpoint_url/name_of_object
    file_name = f"https://sara.hb.kz-ast.vkcs.cloud/{file_name}"
    return file_name


# Чтоб кидать в бинарном варианте
async def s3_uploadobj(file_name, object_name=None):
    if object_name is None:
        object_name = file_name
    try:
        response = s3_client.upload_fileobj(file_name, s3Settings.S3_BUCKET_NAME, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


async def s3_deleteobj(file_name):
    try:
        response = s3_client.delete_object(Bucket=s3Settings.S3_BUCKET_NAME, Key=file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True