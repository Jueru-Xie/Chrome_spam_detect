from __future__ import print_function
from logging import PlaceHolder
import os.path
from re import L, S
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

CLIENT_FILE = 'client.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
def getEmailIds(service, after, before):
    query = "after:"+after+"before:"+before
    ids = service.users().messages().list(userId='me',
                                                q=query).execute()
    
    return ids["messages"]

def filterKeywords(service, ids, keyword):
    update_ids = []
    for id in ids:
        idSpe = id["id"]
        #print(idSpe)
        mailEntity = service.users().messages().get(userId='me',
                                                id=idSpe).execute()
        snippet = mailEntity['snippet']
        if keyword.lower() in snippet.lower():
            update_ids.append(idSpe)
            #print(snippet)
            continue

        headers = mailEntity['payload']['headers']
        for header in headers:
            if keyword.lower() in header['value'].lower():
                update_ids.append(idSpe)
                #print(header['value'])
                break                                         
    print("Scanned " + str(len(ids)) + " emails, found " + str(len(update_ids)) + " target emails")    
    return update_ids

def createLabel(service, labelName):
    label = {
    "labelListVisibility": "labelShow",
    "messageListVisibility": "show",
    "name": labelName}
    newlabel = service.users().labels().create(userId='me', body=label).execute()
    return newlabel['id']

def labelEmails(service, labelId, emailIds):
    body = {
        "addLabelIds": labelId,
        "ids": emailIds,
        }
    service.users().messages().batchModify(userId='me', body = body).execute()

#Create a label, search in the instructed timeframe by keyword and put the 
#emails found to that label
def labelOmni(service, labelName, after, before, keyword):
    ids = getEmailIds(service, after, before)
    filterd_ids = filterKeywords(service, ids, keyword)
    labelId = createLabel(service, labelName)
    labelEmails(service, labelId, filterd_ids)

def labelHandler(labelName, keyword, after, before):
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
    labelOmni(service, labelName, after, before, keyword)

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
    print("in main")
    labelOmni(service, "IPreferMegabus", "2021-11-20", "2021-11-30", "Greyhound")


if __name__ == '__main__':
    main()

