# This function cleans text files from OCR output
# created Wed Dec  2 15:37:56 EST 2015

# libraries
from string import whitespace
from unidecode import unidecode

def basic_clean_list(document_text):
    '''
    given a text document this function splits into a list of lines
    decodes the unicode into utf-8 which is easier to parse

    arg: document with text lines indicated by \n

    returns: list of strings
    '''
    # split into lines
    lines = document_text.split('\n')

    # placeholder for the decoded lines
    clean_lines = []

    # checks to see if line is empty
    # use unidecode to convert lines into utf-8
    # then take out punctuation that is not
    for line in lines:
        decoded_line = unidecode(line)
        clean_lines.append(decoded_line)

    return clean_lines


def space2_split(line):
    '''
    Given a line from a document that has been
    cleaned using the basic_clean function
    splits line into list based on 2+ white space.
    The function then removes the whitespace from this list.
    Finally it joins the lists and returns the line as a string

    arg: string

    returns: string
    '''
    # split string on 2 or more spaces
    words = line.split()

    # #
    clean_words = []

    # remove whitespace from words
    for word in words:
        no_space = words.translate(None, whitespace)
        clean_words.append(no_space)

    return clean_words


def clean_text(text):
    '''
    Given the text of a document that is the result of the OCR process
    used on the League of Nations Documents, this function runs some
    basic processes on the text to improve its accuracy.

    args: text as a string of unicode

    returns: text as a string of utf-8
    '''
    # split into lines and decode to utf-8
    lines = basic_clean_list(text)

    # placeholder for cleaned lines lines
    cleaned_lines = []

    # break into words remove whitespace and put back
    for line in lines:
        words = space2_split(line)
        rejoined_line = ' '.join(words)
        cleaned_lines.append(rejoined_line)

    # join lines with \n spacing
    final_text = '\n'.join(cleaned_lines)

    return final_text


'''
make the unidecode an if statment if it is encoded as unicode

Think about how I might use spellcheck as a feature.`
'''
