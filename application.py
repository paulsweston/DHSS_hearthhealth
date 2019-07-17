from flask import Flask, jsonify, render_template, request
import boto3
import io
import pandas as pd
from bucket import Bucket
import json
import uuid

application = Flask(__name__)

report_bucket = Bucket()

@application.route("/")
def main():
    return render_template("index.html")

@application.route("/account")
def account():
    return render_template("account.html")

@application.route("/basicchat")
def basicchat():
    return render_template("basicchat.html")

@application.route("/answers", methods=['POST'])
def save_answer_to_bucket():
    data = json.loads(request.data)
    csv_array = [
        'Title,Question,Answers'
    ]
    for item in data:
        csv_array.append('"{0}","{1}","{2}"'.format(item.get('title', ''), item.get('question', ''), item.get('answer', '')))

    file_id = str(uuid.uuid4())
    filename = '{0}-input.csv'.format(file_id)
    response = report_bucket.write_file(filename, '\n'.join(csv_array))
    return file_id

@application.route("/report")
def report():
    file_id = request.args.get('id')
    results = []
    if file_id:
        s3 = boto3.resource('s3')
        obj = s3.Object('hearth-health-report','{0}-input.csv'.format(file_id))
        in_file = obj.get()['Body'].read()
        data_df = pd.read_csv(io.BytesIO(in_file), header=0, delimiter=",", low_memory=False)
        data_df=data_df.dropna();
        for index, row in data_df.iterrows():
            print(row['Title'], row['Question'])
            results.append({"title": row['Title'],"question": row['Question'], "message":  row['Answers']})
    return render_template("report.html", results=results)

@application.route('/questions', methods=['GET'])
def send_questions_to_client():
    with open('./questions.json', 'r') as f:
        questions = f.read()
        return questions

if __name__ == "__main__":
    application.run()