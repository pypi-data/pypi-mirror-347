from google.cloud import storage


def upload_file(bucket_name, source_file_path, destination_blob_name):
    """Uploads a file to a GCS bucket."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    return f"Uploaded {source_file_path} to {bucket_name}/{destination_blob_name}"


def list_bucket_files(bucket_name):
    """Lists all files in the bucket."""
    client = storage.Client()
    blobs = client.list_blobs(bucket_name)
    return [blob.name for blob in blobs]
