from flask import Flask, jsonify, render_template, request
from bucket import Bucket
import json
import uuid

application = Flask(__name__)

history = dict()

report_bucket = Bucket()

@application.route("/")
def main():
    return render_template("index.html")

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
        csv_array.append('{0},{1},{2}'.format(item.get('title', ''), item.get('question', ''), item.get('answer', '')))

    filename = '{0}-input.csv'.format(str(uuid.uuid4()))
    response = report_bucket.write_file(filename, '\n'.join(csv_array))
    print(response)

@application.route("/report")
def report():
    return render_template("report.html")

@application.route("/newreport", methods=['GET'])
def newreport():
    return jsonify({"response": history})

@application.route('/questions', methods=['GET'])
def send_questions_to_client():
    with open('./questions.json', 'r') as f:
        questions = f.read()
        return questions

if __name__ == "__main__":
    application.run()