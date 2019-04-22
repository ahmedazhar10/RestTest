import pytest
import quotes_server
import requests
import collections



#---------------POST /reset------------------#

#Resets the state of the server BEFORE each test
#@pytest.fixture(autouse=True)
def reset():
    payload = {}
    request = requests.post('http://127.0.0.1:6543/reset', data=None, json=payload)

reset()
#------------------ GET /quotes --------------------#

def postQuotes(number):
    stored = 0
    for i in range(number):
        info = {"text": "I have a dream"}
        postTheQuote = requests.post('http://127.0.0.1:6543/quotes', data=None, json=info)
        if postTheQuote.ok == True:
            stored = stored + 1
    return stored

def getTotalNumberOfQuotes():
    request = requests.get('http://127.0.0.1:6543/quotes')
    response = request.json()['data']
    return len(response)

req = requests.get('http://127.0.0.1:6543/quotes')

#list of dict
response = req.json()['data']
size = len(response)

#List of IDs
listId = []
for data in response:
    listId.append(data['id'])

# check list is sorted (for atleast 12 quotes)
def isSorted(list):
    sorted = False
    listCopy = list[:]
    listCopy.sort()
    if listCopy == list:
        sorted = True
    return sorted


# Check if there's duplicate
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

#Posting 9 more quotes
print('Quotes posted = ' + str(postQuotes(15)))
#Total number of Quotes, currently
print('Total number of Quotes = ' + str(getTotalNumberOfQuotes()))
print('List is sorted = '+ str(isSorted(listId)))
print('List has duplicate IDs = ' + str(hasDuplicates(listId)))
