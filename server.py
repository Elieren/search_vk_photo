from flask import Flask, request
import json
import io
from search import search

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def content():
    file = request.files['image']
    byte_stream = io.BytesIO()
    byte_stream.write(file.read())

    info = search(byte_stream)
    return info

@app.route('/')
def status():
    return 200

if __name__ == '__main__':
    context = ('server.crt', 'server.key')
    app.run(debug=False, ssl_context=context)