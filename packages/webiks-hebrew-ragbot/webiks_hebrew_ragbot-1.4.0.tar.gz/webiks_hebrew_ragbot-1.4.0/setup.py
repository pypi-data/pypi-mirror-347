from setuptools import setup, find_packages

setup(
    name='webiks-hebrew-ragbot',
    version='1.4.0',
    author='Shmuel Robinov',
    author_email='shmuel_robinov@webiks.com',
    description='A search engine using machine learning models and Elasticsearch for advanced document retrieval.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/shmuelrob/ragbot',
    packages=find_packages(),
    install_requires=[
        'elasticsearch==8.17.1',
        'sentence-transformers==3.4.1',
        'torch==2.6.0',
        'transformers==4.48.3'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    license_files='LICENSE.txt',
    python_requires='>=3.10',
)
