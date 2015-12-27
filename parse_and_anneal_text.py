## Sunday, December 27, 2015
## Parse and Anneal Text
## John Keating
## data.keating@gmail.com

'''
This is a series of functions designd to parse and anneal
the OCR text of the League of Nations archive hosted by the
United Nations at http://search.un.org/results.php?tpl=lon.

As such, it is calibrated for early 20th century
typewriter-written and printed documents, but it could be
used on any OCRed text.

The functions assume that text versions of the documents are
stored in a mongoDB database and the texts are English.
'''


# modules
# import python 3 print and division
from __future__ import print_function, division

# utilities
from numpy import random
import pickle
from random import randint

# pymongo
from pymongo import MongoClient

# text editing
import re
from string import whitespace, digits, punctuation, ascii_letters
from unidecode import unidecode
from fuzzywuzzy import process



# import corpus
from nltk.corpus import brown

#####################################

# create a corpus of English words


brown_set = set([w for w in brown.words()])

#####################################

# Annealing Algorithm
# CITATION needed !!

def segment(text, segs):
    '''
    input: 1. text, a string
           2. segs, a binary string one character fewer
              than the sting

    output: a list of words

    Segment cuts the text string based upon the binary string.
    On every 1 in the binary string segment will cut from the
    begining of the text or from the end of the last cut until the
    equivalent position in the string. It appends the slice
    to the list words. Then it will resume from that position
    making further cuts until the end of segs, the binary string.
    '''
    # empty list for the words
    words = []

    #the last item that was counted
    last = 0

    #split according to segs and append
    for i in range(len(segs)):
        if segs[i] == '1':
            words.append(text[last:i+1])
            last = i+1

    #append the last section to the list
    words.append(text[last:])
    return words


def flip(segs, pos):
    '''
    input: 1. segs, a binary string
           2. pos, a random integer between 0 and the length of
           segs minus one

    returns: a binary string

    Flip takes a randomly generated number pos and uses it to change
    the integer in that string position from 1 to 0 or from 0 to 1.
    '''
    return segs[:pos] + str(1-int(segs[pos])) + segs[pos+1:]

def flip_n(segs, n):
    '''
    input: 1. segs, a binary string
           2. n, an integer

    returns: a binary string

    flip_n takes a binary string and changes integers on the string
    from 1 to 0 or from 0 to 1.
    n is the number of changes that will be made
    '''
    for i in range(n):
        segs = flip(segs, randint(0,len(segs)-1))
        return segs


def evaluate(text, segs):
    '''
    input: 1. text, a string of English text
           2. segs, a binaary string of length one character fewer
           than the length of text

    returns: an integer

    evaluate is still under construction. Sunday, December 27, 2015

    (NB negative values are better than high values)

    evaluate scores one point for each letter in the list of words not
    found in the English corpus and deducts one for each letter in the
    list of words that is.

    '''
    words = segment(text, segs)

    # score for letters not in Brown set
    notset = len(''.join([w for w in words if w not in brown_set]))

    # score for letters not in
    inset = len(''.join([w for w in words if w in brown_set]))
    return notset - inset


def anneal(text, segs, iterations, cooling_rate):
    '''
    input: 1. text, a string of English words
           2. segs, a binary string of length one fewer
           than the length of text
           3. iterations, an integer that determines the number
           of randomly-split strings to be evaluated while the
           temperature is greater than 0.5
           4. cooling_rate, a float greater than 1 that will determine
           how quickly the temperature drops

    returns: a string

    anneal randomly splits a string and assess whether the words formed
    are part of the English lexicon or not (Brown corpus). It stores the
    string with the most words in the English lexicon which will be correct
    or approximately correct
    '''
    temperature = float(len(segs))
    while temperature > 0.5:
        best_segs, best = segs, evaluate(text, segs)
        for i in range(iterations):
            guess = flip_n(segs, int(round(temperature)))
            score = evaluate(text, guess)
            if score < best:
                best, best_segs = score, guess
        score, segs = best, best_segs
        temperature = temperature / cooling_rate
    return segment(text,segs)
