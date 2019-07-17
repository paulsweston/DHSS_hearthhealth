function newload() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var data = xhttp.response;
        var data = data['response'];
        const keys = Object.values(data)
        for (const key of keys) {
            var question = JSON.stringify(key['title']);
            question = question.replace('"', '');
            question = question.replace('"', '');
            h2 = document.createElement('h2');
            h2.innerHTML = question;
            h2.className = "question";
            document.querySelector('#report').append(h2);

            
            var message = JSON.stringify(key['message']);
            message = message.replace('"', '');
            message = message.replace('"', '');
            p = document.createElement('p');
            p.innerHTML = message;
            p.className = 'answer';
            document.querySelector('#report').append(p);
            
        }
    }
  };
  xhttp.open("GET", "/newreport", true);
  xhttp.responseType = 'json';
  xhttp.send();

  
}