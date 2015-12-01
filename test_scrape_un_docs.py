# TEST SCRAPE UN DOCS
# THIS IS A TEST TO GATHER A SMALL AMOUNT OF DOCS

#libraries

import requests
import bs4

def get_soup(url):
    '''
    This function returns a BeautifulSoup object of a website
    when given its url.

    args: url

    returns:
    '''
    response = requests.get(url)
    page =  response.text
    return bs4.BeautifulSoup(page)


def scrape_doc_metadata(soup):
    '''
    This is a function that when given a soup created by Beautiful Soup
    of a UN document search page for the League of Nations
    will scrape all the metadata for the documents. Namely, it will
    scrape the title, the pdf link, the date of publication and the
    languge of a document a list of tuples ready to be converted into
    SON format

    args: soup from BeautifulSoup

    returns: tuple
    '''

    # empty lists
    title_list = []
    link_list = []
    date_list = []
    lang_list = []


    # find all article tags
    arts = soup.findAll('articles')


    # get titles and links from the articles
    for art in arts:
        art_contents = art.findAll('a')
        for content in art_contents:
            title_list.append(content.text)
            link_list.append(content.attrs['href'])

    # get titles and links from the page
    date_lang = soup.findAll('div', attrs={'class': 'fileSize'})

    for contents in date_lang:
        date_list.append(contents.text)
        lang_list.append(contents.findNextSibling().text)

    # clean up title_list and link list
    title_list = [i for i in title_list if i != u'\xa0' and i != '']
    link_list = [i for i in link_list if type(i)
                 == type('') and i.startswith('h') == True]

    return zip(title_list, link_list, date_list, lang_list)



def run_through_un_docs(base_url):
    '''
    This function when given a url will run through all of the UN pages
    returning a list of all the metadata associated with the League of
    nations documents.
    The function runs until it returns an empty soup or the counter reaches
    2000, whichever is first.
    '''
    counter = 1

    all_pages_list = []

    while get_soup(base_url + str(counter)) != 0:
        soup = get_soup(base_url +str(count))

        meta_data = scrape_doc_metadata(soup)

        all_pages_list.append(meta_data)

    return all_pages_list
