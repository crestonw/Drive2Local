import io
from apiclient import http
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

# A dictionary to convert Google Doc MIME types to their Microsoft Office equivalents (or png for images)
MIME_EXPORT = {
	# Google Doc
	"application/vnd.google-apps.document": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
	# Google Slide
	"application/vnd.google-apps.presentation": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
	# Google Drawing
	"application/vnd.google-apps.drawing": "image/png",
	# Google Sheet
	"application/vnd.google-apps.spreadsheet": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
}

# A dictionary of MIME types and their file extensions
MIME_EXTENSIONS = {
	"text/html": ".html",
	"application/zip": ".zip",
	"text/plain": ".txt",
	"application/rtf": ".rtf",
	"application/pdf": ".pdf",
	"application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
	"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
	"text/csv": ".csv",
	"image/jpeg": ".jpg",
	"image/png": ".png",
	"image/svg+xml": ".svg",
	"application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx"
}

def getDrive():
	'''
	Authorizes the app for readonly access to the user's entire Google Drive.
	
	Redirects the user to Google to get a token, then stores the token in a local
	credential store for further use.

	Returns a token representing authorized access to the user's Google Drive.
	'''

	# Define the permission scope (readonly to the entire drive)
	SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
	# Define the local credential store
	store = file.Storage('storage.json')
	# Get credentials from the local store
	creds = store.get()
	# If the credentials do not exist or are invalid, get new credentials from the user
	if not creds or creds.invalid:
	    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
	    creds = tools.run_flow(flow, store)

	# Return the Google Drive of the credentialed user
	return discovery.build('drive', 'v3', http=creds.authorize(Http()))

def getFiles(DRIVE):
	'''
	Returns a list of all files stored in Google Drive that the user has
	read access to.

	The list contains the name, id, and mimeType for each file in it.
	'''

	return DRIVE.files().list().execute()['files']

def getFileMetadata(DRIVE, fileid):
	'''
	Returns a file object populated with all the metadata for that file.
	'''

	return DRIVE.files().get(fields="*",fileId=fileid).execute()

def downloadFile(DRIVE, fileid, filename):
	'''
	Accepts a file ID and filename and attempts to download that file from
	Google Drive.
	'''

	# Create a request for the file to download
	request = DRIVE.files().get_media(fileId=fileid)
	# Open a stream up to write bytes to the given filename
	fh = io.FileIO(filename, 'wb')
	# Create a downloader from the request to the file stream
	downloader = http.MediaIoBaseDownload(fh, request)
	done = False
	# Download chunks of the file until done
	while done is False:
	    status, done = downloader.next_chunk()

def exportFile(DRIVE, fileid, mimetype, filename):
	'''
	Accepts a file ID, mimeType, and filename and attempts to export the
	file from Google Drive to the given mimeType.
	'''

	# Create a request for the file to export
	request = DRIVE.files().export_media(fileId=fileid, mimeType=mimetype)
	# Open a stream up to write bytes to the given filename
	fh = io.FileIO(filename, 'wb')
	# Create a downloader from the request to the file stream
	downloader = http.MediaIoBaseDownload(fh, request)
	done = False
	# Download chunks of the file until done
	while done is False:
	    status, done = downloader.next_chunk()

if __name__ == '__main__':
	# Setup the users Google Drive and save the instance
	DRIVE = getDrive()

	files = getFiles(DRIVE)
	for f in files:
		print(getFileMetadata(DRIVE, f['id']))
#	for f in files:
#		# Handle native Google Drive files
#		if f['mimeType'] in MIME_EXPORT:
#			mimeType = MIME_EXPORT[f['mimeType']]
#			extension = MIME_EXTENSIONS[mimeType]
#			name = f['name']+extension
#			#exportFile(DRIVE, f['id'], mimeType, name)
#			print(name, mimeType)
#		# Handle files uploaded to Google Drive (non-native)
#		else:
#			#downloadFile(DRIVE, f['id'], name)
#			print(name, f['mimeType'])
