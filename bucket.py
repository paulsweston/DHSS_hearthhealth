import boto3
import io
import pandas as pd

class Bucket(object):
    def __init__(self):
        self.name = 'hearth-health-report'
        self.client = boto3.client('s3')

    def write_file(self, filename, data):
        return self.client.put_object(Bucket=self.name, Body=data, Key=filename)


    def read_file(self, filename):
        results = []
        s3 = boto3.resource('s3')
        obj = s3.Object(self.name, filename)
        in_file = obj.get()['Body'].read()
        data_df = pd.read_csv(io.BytesIO(in_file), header=0, delimiter=",", low_memory=False)
        for index, row in data_df.dropna().iterrows():
            results.append({"title": row['Title'], "question": row['Question'], "message":  row['Answers']})
        return results