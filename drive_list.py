from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

def getDrive():
	# Define the permission scope
	SCOPES = 'https://www.googleapis.com/auth/drive.readonly.metadata'
	# Define the local credential store
	store = file.Storage('storage.json')
	# Get credentials from the local store
	creds = store.get()
	# If the credentials are invalid, get new credentials from the user
	if not creds or creds.invalid:
	    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
	    creds = tools.run_flow(flow, store)

	# Get the Google Drive of the credentialed user
	DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

	return DRIVE

def listFiles(DRIVE):
	files = DRIVE.files().list().execute().get('files', [])
	for f in files:
	    print(f['name'], f['mimeType'])

if __name__ == '__main__':
	DRIVE = getDrive()
	listFiles(DRIVE)
