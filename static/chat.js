class Chat {
    constructor() {
        this.questions = []
        this.questionNumber = 0
        this.chatbox = document.querySelector('#message')
        this.chatsubmit = document.querySelector('#send')
        this._disableInputs(true)
    }

    initQuestions() {
        const request = new Request()
        request.get('/questions', (err, data) => {
            if (err) {
                console.log(err)
            }
            else {
                this.questions = JSON.parse(data)
                this._newQuestion()
                this.chatbox.disabled = false
            }
        })
    }

    saveUserInput() {
        var answer = this.chatbox.value
        this.questions[this.questionNumber]['answer'] = answer
        this._addUserResponseToChat(answer)
        this.chatbox.value = ''
        this.questionNumber += 1
        if (this.questionNumber < this.questions.length) {
            this._newQuestion()
        }
        else {
            this._submitAnswer()
        }
    }


    _submitAnswer() {
        this._disableInputs(true)
        const request = new Request()

        request.post('/answers', JSON.stringify(this.questions), (err, fileId) => {
            if (err) {
                console.log(err)
            }
            else {
                var linkToReport = `<a href="/report?id=${fileId}">View your report</a>`
                this._addBotResponseToChat(linkToReport)
            }
        })
    }

    _newQuestion() {
        this._addBotResponseToChat(this.questions[this.questionNumber].question)
    }

    _addBotResponseToChat(msg) {
        const vcard = document.createElement('div');
        var op = '<img src="/static/images/hh-logo.jpg" class="logo" alt="hh">';
        vcard.innerHTML = op;
        vcard.className = 'vcard bio';
        const rep = document.createElement('div');
        rep.innerHTML = msg;
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


    _addUserResponseToChat(msg) {
        const hcard = document.createElement('div');
        var user = '<img src="/static/images/person_1.jpg" class="logo" alt="user">';
        hcard.innerHTML = user;
        hcard.className = 'hcard bio';
        const body = document.createElement('div');
        body.innerHTML = msg;
        body.className = 'reply-body';
        const li = document.createElement('li');
        li.className = 'comment';
        li.appendChild(hcard);
        li.appendChild(body);
        
        //Check the input value
     
        document.querySelector('#messages').append(li);
    }

    _disableInputs(status) {
        this.chatbox.disabled = status
        this.chatsubmit.disabled = status
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const chat = new Chat()
    chat.initQuestions()
    chat.chatbox.disabled = true
    document.querySelector('#send').onclick = () => {
        chat.saveUserInput()
    }

    document.querySelector('#message').addEventListener('keydown', (event) => {
    var input = document.getElementById('message');
        if (event.keyCode === 13 && input.value.length > 1) {
        
            chat.saveUserInput()
        }

        if (input.value.length > 1){
        document.querySelector('#send').disabled = false
        }
        else {document.querySelector('#send').disabled = true
}
        
    })
});
