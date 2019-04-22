import pytest
import quotes_server
import requests
import collections


#---------------POST /reset------------------#
#Reset the state of the server BEFORE each test
#Create Pytest Fixture that creates this request
payload = {}
req2 = requests.post('http://127.0.0.1:6543/reset', data=None, json=payload)
#print(req2.ok)
#print(req2.text)
#print(req2.url)






