import pytest
import quotes_server
import requests
import collections

#----------------HELPER FUNCTIONS-----------------#
# check list is sorted
def isSorted(list):
    sorted = False
    listCopy = list[:]
    listCopy.sort()
    if listCopy == list:
        sorted = True
    return sorted

# Check if there's duplicate items in list
def hasDuplicates(seq):
    seen = {}
    dupes = []
    result = False

    for x in seq:
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.append(x)
            seen[x] += 1
    if len(dupes) > 0:
        result = True

    return result

#Create post requests automatically
def postQuotes(number):
    stored = 0
    for i in range(number):
        info = {"text": "I have a dream"}
        postTheQuote = requests.post('http://127.0.0.1:6543/quotes', data=None, json=info)
        if postTheQuote.ok == True:
            stored = stored + 1
    return stored

#Returns total number of Quotes, currently
def getTotalNumberOfQuotes():
    request = requests.get('http://127.0.0.1:6543/quotes')
    response = request.json()['data']
    return len(response)



#---------------POST /reset------------------#

#Resets the state of the server BEFORE each test
@pytest.fixture(autouse=True)
def reset():
    payload = {}
    request = requests.post('http://127.0.0.1:6543/reset', data=None, json=payload)

