from setuptools import setup, find_packages

setup(
    name='article_reader',
    packges=find_packages(exclude=['test*', 'venv-ar']),
    version='0.0.1',
    description='Send <p> tags to AWS Polly and play it through Flask',
    author='Leo Kavanagh'
)
