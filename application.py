from flask import Flask, jsonify, render_template, request
import linecache
import boto3
import pandas as pd
import io

application = Flask(__name__)

history = dict()

@application.route("/")
def main():
    return render_template("index.html")

@application.route("/basicchat")
def basicchat():
    return render_template("basicchat.html")

@application.route("/chat", methods=['POST'])
def chat():

    qno = int(request.form.get("qno"))
    question = request.form.get("question")
    message = request.form.get("message")

    # Add data to history
    if qno !=1:
        history[qno]= {"question": question, "message": message}

    response = linecache.getline('chatq.txt', qno)
    print(response)
    response = response.rstrip('\n')

    s3 = boto3.resource('s3')

    obj = s3.Object('hearth-health-report', 'test.csv')
    report = obj.get()['body'].read()
    regex_data = pd.read_csv(io.BytesIO(report), header=0, delimiter=",", low_memory=False)

    return jsonify({"response": regex_data.head(10)})

@application.route("/report")
def report():
    return render_template("report.html")

@application.route("/newreport", methods=['GET'])
def newreport():
    return jsonify({"response": history})

if __name__ == "__main__":
    application.run()