from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from email.mime.text import MIMEText
import base64
import email.utils
import json
# If modifying these scopes, delete the file token.json.
#SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES = ['https://mail.google.com/']

def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
  return {
    'raw': raw_message.decode("utf-8")
  }

def send_message(service, user_id, message):
  try:
    message = service.users().messages().send(userId=user_id, body=message).execute()
    print('Message Id: %s' % message['id'])
    return message
  except Exception as e:
    print('An error occurred: %s' % e)
    return None

def get_all_messages(service, label_name):
    print("Fetching emails...")
    labels = service.users().labels().list(userId='me').execute()
    labelId = ""
    for label in labels['labels']:
        if(label['name']==label_name):
            labelId=label['id']
    responses = service.users().messages().list(userId='me',
                                            labelIds=labelId,
                                            maxResults=500).execute()
    ids=[]

    for message in responses['messages']:
        ids.append(message['id'])
    print("There are "+str(len(ids))+" emails with this label")
    return ids

def get_address(service, ids):
    print("Filtering duplicate senders...")
    addresses=[]
    for id in ids:
        responses = service.users().messages().get(userId='me',
                                                id=id).execute()
        headers = responses['payload']['headers']
        for header in headers:
            #print(header["name"])

            if header["name"]=="From":
                address = header["value"]
                #print(address)
                if address not in addresses:
                    addresses.append(address)
        #[21]['value']
        #address = headers[]    
    return addresses

def replierManu(service, addresses, title, body):
    sender = " "
    print ("There are "+str(len(addresses))+" spam senders, sending reply...")

    counter = 1
    for address in addresses:
        msg = create_message(sender, address, title, body)
        try:
            print("Sending reply #" + str(counter))
            counter = counter+1
            send_message(service, 'me', msg)          
        except Exception as e:
            print("Did not succesfully send this reply")
    print("All replies has been sent succesfully")

def reply(service, addresses, file_name):
    with open(file_name) as f:
        replyContent = json.load(f)
        sender = replyContent['sender']
        title = replyContent['title']
        body = replyContent['body']
    address_count = len(addresses)
    print ("There are "+str(address_count)+" spam senders, sending reply...")

    counter = 1
    for address in addresses:
        msg = create_message(sender, address, title, body)
        try:
            print("Sending reply #" + str(counter))
            counter = counter+1
            send_message(service, 'me', msg)          
        except Exception as e:
            print("Did not succesfully send this reply")
    print("All replies has been sent succesfully")

def replyTemp(service, label, template):
    messages = get_all_messages(service, label)
    addresses = get_address(service, messages)
    reply_status = reply(service, addresses, template)
    return reply_status

def replyMenu(service, label, title, body):
    messages = get_all_messages(service, label)
    address = get_address(service, messages)
    reply_status = replierManu(service, address, title, body)
    return reply_status

def replyHandler(labelName, template, title, replyBody, tempType):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    if(tempType=='template'):
        replyTemp(service, labelName, template)
    if(tempType=='manual'):
        replyMenu(service, labelName, title, replyBody)   

def main():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    replyTemp(service,"guac", "reply.json")
   
    
    

if __name__ == '__main__':
    main()




# def create_draft(service, user_id, message_body):
#   try:
#     message = {'message': message_body}
#     draft = service.users().drafts().create(userId=user_id, body=message).execute()

#     print("Draft id: %s\nDraft message: %s" % (draft['id'], draft['message']))

#     return draft
#   except Exception as e:
#     print('An error occurred: %s' % e)
#     return None  