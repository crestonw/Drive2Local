#!/usr/bin/env python3
import src.Drive2LocalAPIAccess, src.Drive2LocalHandleLocal, src.Drive2LocalLogging
from src.Drive2LocalConfig import *



def isOwned(file):
	'''
	Returns a boolean representing whether a file is owned by the user.
	'''

	return file['owners'][0]['me']


def isTrashed(file):
	'''
	Returns a boolean representing whether a file has been trashed.
	'''

	return file['trashed']


def isFilteredExtension(file):
	'''
	Checks whether or not the file extension is in the filtered list.
	'''

	try:
		if isGoogleFile(file):
			mimeType = src.Drive2LocalAPIAccess.MIME_EXPORT[file['mimeType']]
			exten = src.Drive2LocalAPIAccess.MIME_EXTENSIONS[mimeType]
		else:
			exten = file['fileExtension']
	except:
		return False

	return exten in filetypes


def isGoogleFile(file):
	'''
	Checks whether or not the file is a native Google file (as opposed
	one updloaded to Google Drive)
	'''

	return file['mimeType'] in src.Drive2LocalAPIAccess.MIME_EXPORT


def main():
	# Setup logger

	Drive_logger = src.Drive2LocalLogging.setupLogger()
	
	# Setup the users Google Drive and save the instance
	DRIVE = src.Drive2LocalAPIAccess.getDrive()
	# Get a listing of all files the user has access to
	files = src.Drive2LocalAPIAccess.getFiles(DRIVE, Drive_logger)

	path = src.Drive2LocalHandleLocal.buildDir()
	print(backup_root)
	print(log_root)

	# Download loop
	for f in files:
		# FILTERING
		if owner_filter:
			if not isOwned(f):
				continue
		if not trash_filter:
			if isTrashed(f):
				continue
		if filetype_filter:
			if not isFilteredExtension(f):
				continue

		# DOWNLOADING
		try:
			if isGoogleFile(f):
				if src.Drive2LocalHandleLocal.writeGoogleFile(DRIVE, path, f, Drive_logger) == 1:
					break
			else:
				if src.Drive2LocalHandleLocal.writeFile(DRIVE, path, f, Drive_logger) == 1:
					break
		except KeyboardInterrupt:
			break

	# Compress the newly created backup
	src.Drive2LocalHandleLocal.compressDir(path)

	if rotation_on:
		src.Drive2LocalHandleLocal.rotateBackups(Drive_logger)

	Drive_logger.info("Backup Complete")

if __name__ == '__main__':
	main()
