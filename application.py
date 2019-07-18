from flask import Flask, jsonify, render_template, request
from bucket import Bucket
from formatter import Formatter
from nlp import LanguageProcessor
import json
import uuid
import datetime

application = Flask(__name__)

report_bucket = Bucket()
formatter = Formatter()
language_processor = LanguageProcessor()

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


    date = datetime.datetime.now().strftime('%Y-%m-%d')
    file_id = '{0}_{1}'.format(date, str(uuid.uuid4()))
    filename = '{0}.csv'.format(file_id)
    response = report_bucket.write_file(filename, '\n'.join(csv_array))
    return file_id

@application.route("/report")
def report():
    file_id = request.args.get('id')
    results = []
    if file_id:
        filename = '{0}.csv'.format(file_id)
        wordcloud = '{0}.png'.format(file_id)
        results = report_bucket.read_file(filename)
        answers = formatter.format_answers(results)
        language_processor.generate_word_cloud(answers, wordcloud)
        with open(wordcloud, 'r') as f:
            data = f.read()
            report_bucket.write_file(wordcloud, data)
    return render_template("report.html", results=results)

@application.route('/questions', methods=['GET'])
def send_questions_to_client():
    with open('./questions.json', 'r') as f:
        questions = f.read()
        return questions

if __name__ == "__main__":
    application.run()