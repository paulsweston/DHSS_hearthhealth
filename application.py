from flask import Flask, jsonify, render_template, request
import linecache

application = Flask(__name__)

history = dict()

@application.route("/")
def main():
    return render_template("index.html")

@application.route("/account")
def account():
    return render_template("account.html")

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
    return jsonify({"response": history})

if __name__ == "__main__":
    application.run()