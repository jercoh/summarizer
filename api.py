from flask import Flask, request, jsonify, render_template, Markup
from flask_restful import reqparse, abort, Api, Resource
from summarizer import Summarizer


app = Flask(__name__, static_url_path = "")
app.config["CACHE_TYPE"] = "null"

base_url = '/summarizer/'

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.route(base_url+'summarize', methods = ['GET'])
def summarize():
    url = request.args.get('url')
    summarizer = Summarizer(url)
    if url != False:
    	summary = summarizer.summarize()
    	response = {'title': summarizer.title, 'summary': summary, 'img': summarizer.article.top_image}
    	return jsonify(response)
    raise InvalidUsage('Oops something got wrong. Please try again', status_code=404)

@app.route('/', methods = ['GET'])
def root():
    return render_template('index.html'), 200

@app.route('/post', methods = ['GET'])
def post():
    try:
        url = request.args.get('url')
        summarizer = Summarizer(url)
        return render_template('post.html', text=Markup(summarizer.summarize()), img= summarizer.article.top_image, title=summarizer.title), 200
    except:
        raise InvalidUsage('Oops something got wrong. Please try again', status_code=404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
