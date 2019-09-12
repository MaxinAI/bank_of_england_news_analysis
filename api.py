"""Flask Api Service"""
import argparse
import json
import warnings

from flask import Flask, request
from waitress import serve

from model.data_extraction import DataExtractor

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument('--host', default='0.0.0.0', help="server host")
parser.add_argument('--port', default='5000', help="server port")
parser.add_argument('--query_key', default='text', help="default query key name for GET request")
parser.add_argument('--debug', action="store_true", help="enable debugging")
parser.add_argument('--logging', action="store_true", help="enable logging")
parser.add_argument('--log_file', default='logs.txt', help="log file name")

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def info():
    """
    Gets POST or GET request containing bank news text string or list of strings, analyses them and returns
    json formatted result containing original news text, found bank rate and quantitative easing number if exists.

    Returns:
        response: (list) containing dictionaries with keys: [news, Bank_Rate, QE]

    """
    response = json.dumps({}, ensure_ascii=False)
    if request.method == 'GET':
        text = request.args.get(args.query_key)
        if text is not None:
            results = data_extractor.analyse(text)
            response = json.dumps(results, ensure_ascii=False)

    elif request.method == 'POST':
        data = json.loads(request.data.decode())
        if data is not None and isinstance(data, list):
            results = data_extractor.analyse(data)
            response = json.dumps(results, ensure_ascii=False)

    if args.logging:
        with open(args.log_file, 'a') as file:
            file.write(response + "\n")
    return response


if __name__ == '__main__':
    args = parser.parse_args()

    data_extractor = DataExtractor()

    if args.debug:
        app.run(host=args.port, port=args.port, debug=True)
    else:
        serve(app.wsgi_app, host=args.host, port=args.port, threads=True)
