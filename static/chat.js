document.addEventListener('DOMContentLoaded', () => {
    
    // Set session question number
    var qno = 1;

    //Create global question
    var question;

    //Disable the send button
    document.querySelector('#send').disabled = true;

    // Check the theres is a message to send
    document.querySelector('#message').onkeyup = () => {
        if (document.querySelector('#message').value.length > 0)
            document.querySelector('#send').disabled = false;
        else
            document.querySelector('#send').disabled = true;
    };
    
    document.querySelector('#form').onsubmit = () => {
        const message = document.querySelector('#message').value;
        
        // Create a new line item for the message
        
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

        //Add message to chat list
        document.querySelector('#messages').append(li);

        // Start new request
        const request = new XMLHttpRequest();
        request.open('POST', '/chat');

        // Callback funciton when request completes
        request.onload = () => {

            // Callback when returned
            const data = JSON.parse(request.responseText);
            question = data.response;

            //update new question item
            const vcard = document.createElement('div');
            var op = '<img src="/static/images/hh-logo.jpg" class="logo" alt="hh">';
            vcard.innerHTML = op;
            vcard.className = 'vcard bio';
            const rep = document.createElement('div');
            rep.innerHTML = data.response;
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
        
        // Add data to send with request
        const data = new FormData();
        data.append('message', message);
        data.append('qno', qno);
        data.append('question', question)

        // Send request
        request.send(data);
    
        //Clear field
        document.querySelector('#message').value = '';
        // Disable the send button
        document.querySelector('#send').disabled = true;
        // Update Question counter
        qno ++;
        return false;
    };
    
});