import os
import datetime as dt
import requests
from lxml import html
import boto3


def get_text(url):
    """
    Read a full web page, extract text from <p> tags
    :param url: string
    :return: string
    """

    page = requests.get(url)
    tree = html.fromstring(page.content)

    text = ' '.join(tree.xpath('//p/text()')) \
            .replace('\n', '') \
            .replace('\t', '') \
            .split('\xa0')[0]

    print(text)
    return text



def extract_sentences(text):
    """
    Return a list of strings resulting from splitting the input string
    any full stop followed by a space.

    This isn't an NLP project, so that'll do for now.

    :param text: str
    """

    sentences = text.split(". ")

    return sentences


def chunk(sentence, max_len=1500):
    """
    Rewriting the recursive pattern matched monstrosity in the Scala
    version of this app.

    if sentence length (in chars) < max_len, return the full sentence

    else split on spaces (loosely-speaking into words) and then
    recombine into a list of two strings, containing the first and second
    halves of the sentence respectively.

    Then apply chunk_sentences to those two substrings and combine the
    resultant lists

    Note: if the max_len is less than the number of letters in any given
    word in the original sentence you'll probably get a recursion error.

    :param sentence: str
    :return list of strings
    """

    if len(sentence) <= max_len:
        return sentence

    else:
        word_list = sentence.split(' ')
        split_point = int(len(word_list)/2)

        first_half = ' '.join(a for a in word_list[0:split_point])
        second_half = ' '.join(a for a in word_list[split_point:])

        return chunk(first_half, max_len) + chunk(second_half, max_len)


def get_polly():

    polly_client = boto3 \
        .Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                 aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                 region_name='eu-west-1') \
        .client('polly')

    return polly_client


def synthesise_speech(polly_client, text, voice_id='Brian', output_format='mp3'):
    """
    """

    synth = polly_client \
        .synthesize_speech(VoiceId=voice_id,
                           OutputFormat=output_format,
                           Text=text)

    return synth


def get_speech_streams(polly_client, chunked_sentences):
    """
    """

    res = list(map(lambda x: synthesise_speech(polly_client, x),
               chunked_sentences))

    return res


def save_streams(streams, outfile=os.path.join(os.path.dirname(__file__), 'static/audio/article.mp3')):
    """
    """

    try:
        os.remove(outfile)
    except Exception as e:
        print('{}: {}', type(e), e)

    data = []
    with open(outfile, 'ab') as f:
        for stream in streams:
            f.write(stream['AudioStream'].read())
            stream['AudioStream'].close()


def run_article_reader(url):
    """
    """

    polly_client = get_polly()

    text = get_text(url)

    sentences = extract_sentences(text)

    chunks = list(map(chunk, sentences))

    streams = get_speech_streams(polly_client, chunks)

    save_streams(streams)

