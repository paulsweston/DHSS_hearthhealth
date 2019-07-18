class Request {
    constructor() {
        this.request = new XMLHttpRequest()
    }

    get(url, callback) {
        this.request.open('GET', url)

        this.request.onreadystatechange = () => {
            if (this.request.readyState === 4) {
                if (this.request.status === 200) {
                    callback(null, this.request.responseText)
                }
                else {
                    callback(this.request.statusText, null)
                }
            }

        }

        this.request.send()
    }

    post(url, data, callback) {
        this.request.open('POST', url)

        this.request.onreadystatechange = () => {
            if (this.request.readyState === 4) {
                if (this.request.status === 200) {
                    callback(null, this.request.responseText)
                }
                else {
                    callback(this.request.statusText, null)
                }
            }
        }

        this.request.onerror = () => {
            console.log('error')
        }

        this.request.send(data)
    }
}