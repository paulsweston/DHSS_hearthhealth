import boto3
import io

class Bucket(object):
    def __init__(self):
        self.name = 'hearth-health-report'
        self.client = boto3.client('s3')

    def write_file(self, filename, data):
        return self.client.put_object(Bucket=self.name, Body=data, Key=filename)


    def read_file(self, filename):
        bytes_buffer = io.BytesIO()
        client.download_fileobj(Bucket=self.name, Key=filename, Fileobj=bytes_buffer)
        byte_value = bytes_buffer.getvalue()
        return byte_value.decode()