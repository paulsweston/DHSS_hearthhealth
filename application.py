from flask import Flask, jsonify, render_template, request
from bucket import Bucket
from formatter import Formatter
from nlp import LanguageProcessor
from sentiment import SentimentAnalyzer
import json
import boto3
import uuid
import datetime

application = Flask(__name__)

report_bucket = Bucket()
formatter = Formatter()


@application.route("/")
def main():
    return render_template("index.html")

@application.route("/account")
def account():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hearth-health-report')
    reports = bucket.objects.all()
    output = []
    for report in reports:
        if ".csv" in report.key:
            report_title = report.key.split("_", 1)[0]
            output.append({
                'title': report_title,
                'link': report.key.replace('.csv', '')
            })
    return render_template("account.html", reports=output)

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


    date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file_id = '{0}_{1}'.format(date, str(uuid.uuid4()))
    filename = '{0}.csv'.format(file_id)
    response = report_bucket.write_file(filename, '\n'.join(csv_array))
    return file_id

@application.route("/report")
def report():
    file_id = request.args.get('id')
    results = []
    if file_id:
        language_processor = LanguageProcessor()
        sentiment_analyzer = SentimentAnalyzer()
        filename = '{0}.csv'.format(file_id)
        wordcloud = '{0}.png'.format(file_id)
        sentiment_file = '{0}-sentiment.jpg'.format(file_id)
        results = report_bucket.read_file(filename)
        answers = formatter.format_answers(results)
        language_processor.generate_word_cloud(answers, wordcloud)
        sentiment_analyzer.generate_sentiment_graph(answers, sentiment_file)
        report_bucket.upload_file(wordcloud)
        report_bucket.upload_file(sentiment_file)
    return render_template("report.html", results=results, file=file_id)

@application.route('/questions', methods=['GET'])
def send_questions_to_client():
    with open('./questions.json', 'r') as f:
        questions = f.read()
        return questions

if __name__ == "__main__":
    application.run()