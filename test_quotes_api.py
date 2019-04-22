import pytest
import quotes_server
import requests
import collections



#def cal(a,b):
#    return a + b

#to skip a test, have the following annotation
#@pytest.mark.skip(reason="lemme skip")
#def test_cal():
#   result = cal(2,3)
#    assert result == 4

#@pytest.mark.parametrize()
#def test_cal(test_input, expected_output):
#    result = cal()

#------------------ GET /quotes --------------------#

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

#print(isSorted(listId))
#print(hasDuplicates(listId))


#---------------POST /reset------------------#
#Reset the state of the server BEFORE each test
#Create Pytest Fixture that creates this request
payload = {}
req2 = requests.post('http://127.0.0.1:6543/reset', data=None, json=payload)
#print(req2.ok)
#print(req2.text)
#print(req2.url)

#-----------------POST /quotes-------------------#

# Accepts a new quote and assigns new ID
payload = {"text": "I have a dream"}
postQuote = requests.post('http://127.0.0.1:6543/quotes',data=None,json=payload)
#print(postQuote.ok) #True
#print(postQuote.text)
#print(postQuote.json()['data']['id']) #The ID == 4 (asserted value)

# Rejects missing text
payload2 = {}
rejectMissingField = requests.post('http://127.0.0.1:6543/quotes',data=None,json=payload2)
#print(rejectMissingField.ok) #False
#print(rejectMissingField.text)
#print(rejectMissingField.status_code) # HTTP code = 400

#Rejects integer values
payload3 = {"text": 123}
rejectInteger = requests.post('http://127.0.0.1:6543/quotes',data=None,json=payload3)
#print(rejectInteger.ok) #False
#print(rejectInteger.text)
#print(rejectInteger.status_code) # HTTP code = 400

#Stores 20 quotes
for i in range(20):
    info = {"text": "I have a dream"}
    postTheQuote = requests.post('http://127.0.0.1:6543/quotes', data=None, json=info)

res = requests.get('http://127.0.0.1:6543/quotes')
repondre = res.json()['data']
size = len(repondre)
#print(size) # size > 20

# After adding quotes, should appear in GET /quotes
payload40 = {"text": "I have a dream"}
addQuote = requests.post('http://127.0.0.1:6543/quotes',data=None,json=payload40)
newId = addQuote.json()['data']['id']
print(addQuote.ok) # True

#should retrieve on Get /quotes/id
returnNewQuote = requests.get('http://127.0.0.1:6543/quotes/'+str(newId))
#print(returnNewQuote.ok) #True

#Should appear on Get /quotes
newQuotes = requests.get('http://127.0.0.1:6543/quotes/')
listNewQuotes = newQuotes.json()['data']
yourQuote = listNewQuotes[newId-1]
print(yourQuote) #{"id": newId, "text": "I have a dream"}


#------------------GET /quotes/<id>---------------#
inputId = 2
getQuote = requests.get('http://127.0.0.1:6543/quotes/'+str(inputId))

allQuotes = requests.get('http://127.0.0.1:6543/quotes')
listAllQuotes = allQuotes.json()['data'] #List of all Quotes retrieved from  GET '/quotes'
sizeQuotes = len(listAllQuotes)

listIndiQuotes = [] #List of quotes retrieved individually
#Get quote one by one
for i in range(1, (sizeQuotes+1)):
    response = requests.get('http://127.0.0.1:6543/quotes/'+str(i))
    quote = response.json()['data']
    listIndiQuotes.append(quote)

#Check if both lists match
#print(listAllQuotes == listIndiQuotes) #True
#print(listIndiQuotes)
#print(listAllQuotes)



#Nonexistant ID
invalidID = 5
invalidResponse = requests.get('http://127.0.0.1:6543/quotes/'+str(invalidID))
#print(invalidResponse.ok) #False
#print(invalidResponse.status_code) #HTTP Code = 404

#----------------DELETE/quotes------------------#
original = requests.get('http://127.0.0.1:6543/quotes')
id = 1
deleted = requests.delete('http://127.0.0.1:6543/quotes/'+str(id))
#print(deleted.ok) #True
#print(deleted.text)

#Check if it gives error on deleting the same thing twice or more times
deleteTwice = requests.delete('http://127.0.0.1:6543/quotes/'+str(id))
#print(deleteTwice.ok) #False
#print(deleteTwice.text) #No such resource
#print(deleteTwice.status_code) #HTTP code = 404

#Check ID still exists by passing ID
response = requests.get('http://127.0.0.1:6543/quotes'+str(id))
#print(response.ok) #False

#Check if ID still exists in list of Quotes
response = requests.get('http://127.0.0.1:6543/quotes')
#print(original.text == response.text) #False

