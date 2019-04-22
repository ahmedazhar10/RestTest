import requests

#GET Request
#r = requests.get('https://xkcd.com/353/')

#image = requests.get('https://imgs.xkcd.com/comics/python.png')
#with open('comic.png', 'wb') as f:
#    f.write(image.content)

#print(image.status_code)
# response error
# 200 = success
# 400 = client errors
# 300 = redirect
# 500 = server error

#Check if everything is ok
#print(image.ok)


#Shows you all the attributes and methods
#print(dir(r))

#Shows you more info about r
#print(help(r))

#returns the html code
#print(r.text)

#Download an image


# INTRODUCING GET requests

payload = {'page': 2, 'count': 25}
req = requests.get('https://httpbin.org/get', params=payload)

print(req.text)
print(req.url)

# POST Requests

payload2 = {'username': 'Corey', 'password': 'testing'}
req2 = requests.post('https://httpbin.org/post', data=payload2)

print(req2.text)
print(req2.url)

#look at the HTML source code of the URL to see
# what values that form expects

req_dict = req2.json()
print(req_dict['form'])