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


#------------------ GET /quotes --------------------#

# Tests if output data is sorted by ID (for atleast 12 quotes)
#BUG FOUND = IDs are only sorted for up to 9 Quotes in total
#@pytest.mark.skip(reason="lemme skip")
def test_are_IDs_sorted():

    result = False

    #Creating and Posting 9 more Quotes
    #to have 12 quotes in total
    postQuotes(9)

    #Get all quotes
    req = requests.get('http://127.0.0.1:6543/quotes')

    # list of dict
    response = req.json()['data']
    size = len(response)

    # List of IDs
    listId = []
    for data in response:
        listId.append(data['id'])

    #Checking if IDs are sorted
    assert isSorted(listId) == True

#Test if there are duplicate ID's
#Result: IDs never duplicate
def test_duplicateIDs_exist():

    # Creating and Posting 9 more Quotes
    postQuotes(9)

    # Get all quotes
    req = requests.get('http://127.0.0.1:6543/quotes')

    #list of dict
    response = req.json()['data']
    size = len(response)

    #List of IDs
    listId = []
    for data in response:
        listId.append(data['id'])

    assert hasDuplicates(listId) == False

#-----------------POST /quotes-------------------#

# Test if it Accepts a new quote and assigns new ID
def test_postNewQuote():
    payload = {"text": "I have a dream"}
    postQuote = requests.post('http://127.0.0.1:6543/quotes',data=None,json=payload)
    quoteID = postQuote.json()['data']['id']
    assert postQuote.ok == True
    assert quoteID == 4

# Test if it Rejects missing text, on posting Quote
def test_MissingText():
    payload = {}
    errorMessage = 'Missing required field "text"'
    rejectMissingField = requests.post('http://127.0.0.1:6543/quotes',data=None,json=payload)
    assert rejectMissingField.ok == False
    assert rejectMissingField.json()['error'] == errorMessage
    assert rejectMissingField.status_code == 400 # HTTP code = 400

#Test if it Rejects integer valuesm on posting a Quote
def test_RejectInteger():
    payload = {"text": 123}
    errorMessage = 'Invalid type for field "text", expected string'
    rejectInteger = requests.post('http://127.0.0.1:6543/quotes',data=None,json=payload)
    assert rejectInteger.ok == False
    assert rejectInteger.json()['error'] == errorMessage
    assert rejectInteger.status_code == 400 # HTTP code = 400

#Test if it stores 20 quotes or more
#BUG FOUND: Can only support upto 18 Quotes in total
#@pytest.mark.skip(reason="lemme skip")
def test_storeMoreThan20Quotes():

    #Posting 17 new Quotes
    posted = postQuotes(17)
    assert posted == 17

    #Check total quotes == 20
    request = requests.get('http://127.0.0.1:6543/quotes')
    response = request.json()['data']
    assert len(response) == 20

#Test if Quote is retrieved after adding
def test_getNewlyAddedQuote_byID():
    #Posting new Quote
    payload = {"text": "I have a dream"}
    addQuote = requests.post('http://127.0.0.1:6543/quotes',data=None,json=payload)
    newId = addQuote.json()['data']['id'] #ID == 4
    assert addQuote.ok == True

    #Retrieve on Get /quotes/id
    returnNewQuote = requests.get('http://127.0.0.1:6543/quotes/'+str(newId))
    assert returnNewQuote.ok == True

#Test if Quote appears on Get /quotes
def test_NewQuote_updatesAllQuotes():
    #Posting new Quote
    payload = {"text": "I have a dream"}
    addQuote = requests.post('http://127.0.0.1:6543/quotes',data=None,json=payload)
    newId = addQuote.json()['data']['id'] #ID == 4
    assert addQuote.ok == True

    #Quotes on Get /quotes
    updatedQuotes = requests.get('http://127.0.0.1:6543/quotes')
    listNewQuotes = updatedQuotes.json()['data']
    newQuote = {"id": newId, "text": "I have a dream"}
    assert newQuote == listNewQuotes[newId-1] #Quote is found
    #print(newQuote) #{"id": newId, "text": "I have a dream"}


#------------------GET /quotes/<id>---------------#

#Test if returns Quote using valid ID
def test_getQuoteByID():
    inputId = 2
    getQuote = requests.get('http://127.0.0.1:6543/quotes/'+str(inputId))
    assert getQuote.ok == True

#Test if Quote is retrieved by ID and its text matches
def test_getIDandTextMatch():

    #Quotes from Get /quotes
    allQuotes = requests.get('http://127.0.0.1:6543/quotes')
    listAllQuotes = allQuotes.json()['data'] #List of all Quotes retrieved from  GET '/quotes'
    sizeQuotes = len(listAllQuotes)

    #Quotes from Get /quotes/<id>
    listIndiQuotes = [] #List of quotes retrieved individually
    #Get quote one by one
    for i in range(1, (sizeQuotes+1)):
        response = requests.get('http://127.0.0.1:6543/quotes/'+str(i))
        quote = response.json()['data']
        listIndiQuotes.append(quote)

    assert listAllQuotes == listIndiQuotes

#Test if we get an error response on passing nonexistant ID
def test_NonexistantID():
    invalidID = 5
    invalidResponse = requests.get('http://127.0.0.1:6543/quotes/'+str(invalidID))
    assert invalidResponse.ok == False
    assert invalidResponse.status_code == 404 #HTTP Code = 404

#----------------DELETE/quotes------------------#

#Test if quote is deleted by passing its ID
def test_deleteQuoteByID():
    id = 1
    deleted = requests.delete('http://127.0.0.1:6543/quotes/'+str(id))
    assert deleted.ok == True

#Test if it gives an error on deleting the same ID twice
def test_deleteSameIDAgain():
    id = 1
    deleted = requests.delete('http://127.0.0.1:6543/quotes/'+str(id))
    deleteAgain = requests.delete('http://127.0.0.1:6543/quotes/' + str(id))
    assert deleteAgain.ok == False
    assert deleteAgain.status_code == 404

#Test if it gives error on deleting the same ID more than two times
def test_deleteSameIDFiveTimes():
    id = 1
    deleted = requests.delete('http://127.0.0.1:6543/quotes/' + str(id))
    failed = 0
    for i in range(5):
        deleteAgain = requests.delete('http://127.0.0.1:6543/quotes/'+str(id))
        if deleteAgain.ok == False:
            failed = failed + 1
    assert failed == 5

#Test if Quote does not exist on Get /quotes/<id> i.e. GET Request invalid by passing ID
def test_QuoteDoesNotExist_byID():
    id = 1
    deleted = requests.delete('http://127.0.0.1:6543/quotes/' + str(id))
    response = requests.get('http://127.0.0.1:6543/quotes'+str(id))
    assert response.ok == False

#Test if Quote does not exist in GET /quotes
def test_QuoteDoesNotExist_onAllQuotes():
    #Response before deleting Quote
    original = requests.get('http://127.0.0.1:6543/quotes')
    #Deleting Quote
    id = 1
    deleted = requests.delete('http://127.0.0.1:6543/quotes/' + str(id))
    #Response after deleting Quote
    response = requests.get('http://127.0.0.1:6543/quotes')
    assert original.text != response.text



