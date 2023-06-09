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

    data = search(byte_stream)
    return data

@app.route('/')
def status():
    return '1'

if __name__ == '__main__':
    app.run()