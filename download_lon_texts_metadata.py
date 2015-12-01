# Get League of Nations text and metadata
# from the UN Apache database
# created: Tue Dec  1 11:39:11 EST 2015


# libraries
from urllib2 import urlopen
from pymongo import MongoClient
from time import sleep

base_url = 'http://search.un.org/direct.php?&tpl=lon&query=*:*&wt=python&rows=1&start=1'

def get_doc_data(url):
    '''
    This is a function that downloads league of nation data
    from the UN and retrns it as a standard dictionary
    by default it starts at 1 (first document in search)
    and downloads 100 rows from the database with a query for
    all document in the database.

    args: url

    returns: list of dictionaries
    '''

    connection = urlopen(url)
    response = eval(connection.read())
    docs = response['response']['docs']

    return docs


def add_to_mongo(docs):
    '''
    This function given a list of dictionary, or dictionary like objects
    will insert each one to my mongodb database-collection

    args:
    '''
    counter = 0

    client = MongoClient()

    db = client.lon_db

    coll = db.lon_docs

    for doc in docs:
        coll.insert_one(doc)
        counter += 1

    print 'inserted ' + str(counter) + ' documents'


def build_urls(base_url='http://search.un.org/direct.php?&tpl=lon&query=',
              query='*:*', start=0, rows=100, number=2000):
    '''
    This function will build a list of all urls based on a search query of
    the League of Nations archival apache database.

    args:

    returns: list of url strings
    '''

    rows_s = '&wt=python&rows=' + str(rows) + '&start='

    url_list = []

    for i in range(number/rows):
        url = base_url + query + rows_s + str(start)
        url_list.append(url)
        start += rows

    return url_list


def run_through_urls(url_list):
    '''
    given a list of urls this function will take each in turn
    and input the retuned data into a mongoDB database

    '''

    for url in url_list:
        docs = get_doc_data(url)
        if docs == []:
            print 'completed'
            break
        else:
            add_to_mongo(docs)
            sleep(5)
