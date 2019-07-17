from flask import Flask, jsonify, render_template, request
import linecache
import boto3 
import io
import pandas as pd

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
        
    if len(response) < 1:
        response = "Click <a href='/report'>here</a> to view your report ready for your consulation!"

    return jsonify({"response": response})

@application.route("/report")
def report():
     return render_template("report.html")

@application.route("/newreport", methods=['GET'])
def newreport():
    s3 = boto3.resource('s3')
    obj = s3.Object('hearth-health-report','51d4bcb0-a892-11e9-9087-abfdcf97b62d.csv')
    in_file = obj.get()['Body'].read()
    data_df = pd.read_csv(io.BytesIO(in_file), header=0, delimiter=",", low_memory=False)
    data_df=data_df.dropna();
    for index, row in data_df.iterrows():
        print(row['Title'], row['Question'])
        history[index]= {"title": row['Title'],"question": row['Question'], "message":  row['Answers']}
    return jsonify({"response": history})

if __name__ == "__main__":
    application.run()