import os
from flask import Flask, request, render_template, redirect
import datetime as dt
import requests
from lxml import html
import operator
import functools
import boto3
from logging import Logger
from article_reader import run_article_reader

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('article')

@app.route('/article', methods=['GET', 'POST'])
def article():

    logger = Logger('article-reader')
    if request.method == 'POST':
        url = request.form.to_dict()['articleurl']
        print('url is {}'.format(url))
        run_article_reader(url)

        return redirect('play')

    return render_template('article.html')

@app.route('/play')
def play():

    return render_template('play_article.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

