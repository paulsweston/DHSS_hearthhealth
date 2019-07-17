var questionNumber = 0
var questions = []

function addQuestionToChat(question) {
    const vcard = document.createElement('div');
    var op = '<img src="/static/images/hh-logo.jpg" class="logo" alt="hh">';
    vcard.innerHTML = op;
    vcard.className = 'vcard bio';
    const rep = document.createElement('div');
    rep.innerHTML = question;
    rep.className = 'comment-body';
    const res = document.createElement('li');
    res.className = 'comment';
    res.appendChild(rep);
    res.appendChild(vcard);

    //Add message to chat list
    document.querySelector('#messages').append(res);
    var elemnt = document.getElementById("send")
    elemnt.scrollIntoView(false);
}

function addAnswerToChat(message) {
    const hcard = document.createElement('div');
    var user = '<img src="/static/images/person_1.jpg" class="logo" alt="user">';
    hcard.innerHTML = user;
    hcard.className = 'hcard bio';
    const body = document.createElement('div');
    body.innerHTML = message;
    body.className = 'reply-body';
    const li = document.createElement('li');
    li.className = 'comment';
    li.appendChild(hcard);
    li.appendChild(body);

    document.querySelector('#messages').append(li);
}

function getQuestion() {
    return `${questions[questionNumber].question}?`
}

function initQuestions() {
    const request = new XMLHttpRequest()
    request.open('GET', '/questions')

    request.onload = () => {
        questions = JSON.parse(request.responseText)
        addQuestionToChat(getQuestion())
    }

    request.send()
}

function submitAnswers() {
    const request = new XMLHttpRequest()
    request.open('POST', '/answers')

    request.onload = () => {
        var linkToReport = `<a href="/report">${request.responseText}</a>`
        addQuestionToChat(linkToReport)
    }

    request.send(JSON.stringify(questions))
}

document.addEventListener('DOMContentLoaded', () => {
    initQuestions()

    document.querySelector('#send').onclick = () => {
        const textarea = document.querySelector('#message')
        var answer = textarea.value
        questions[questionNumber]['answer'] = answer
        addAnswerToChat(answer)
        textarea.value = ''
        questionNumber += 1
        if (questionNumber < questions.length) {
            addQuestionToChat(getQuestion())
        }
        else {
            submitAnswers()
        }
    }
});