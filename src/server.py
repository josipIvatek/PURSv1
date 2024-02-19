from flask import Flask, request, make_response


app = Flask("Test za seminar")

@app.post('/rfid')
def post_rfid():
    response = make_response()
    nuid = request.data.decode("utf-8")
    print(nuid)

    response.data = 'Uspješno ste postavili NUID'
    response.status_code = 201
    return response

@app.get('/')
def get_zahtjev():
    response = request.get('http://192.168.223.113/')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

