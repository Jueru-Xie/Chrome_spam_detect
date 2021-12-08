from Google import Create_Service
import json

CLIENT_FILE = 'client.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

#results = service.users().getProfile(userId='me').execute()
#results = service.users().labels().list(userId='me').execute()
results = service.users().settings().getLanguage(userId='me').execute()

def add5(listofN, x):
    listofN.append(x)

array = []

array.append(5)
print(array)
for x in range(0,3):
    add5(array, x)

print(array)

data = {
  "att1":"a",
  "att2":"b"
}

print(data['att1'])
import json

with open('reply.json') as f:
  data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print(data['sender'])