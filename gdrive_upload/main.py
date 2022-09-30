from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import mimetypes
from googleapiclient.errors import HttpError


#variables
id = os.environ['ID']


def main():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()

    elif gauth.access_token_expired:
        gauth.Refresh()

    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)


    cwd = os.getcwd()
    try:
        for root, dirs, files in os.walk(cwd):
            for file in files:
                if file.endswith((".xml", ".json")) and not file.startswith(("client_secrets","mycreds")):
                    file_path=(os.path.join(root, file))
            #print(file_path)
                    head_tail = os.path.split(file_path)

                    mime_type=mimetypes.MimeTypes().guess_type(file_path)[0]

            #print(mime_type)
                    file_upload = drive.CreateFile({"mimeType": f"{mime_type}", "parents": [{"kind": "drive#fileLink", "id": id}]})
                    file_upload['title'] = head_tail[1]
                    file_upload.SetContentFile(file_path)
                    file_upload.Upload(param={'supportsTeamDrives': True}) # Upload the file.

                    print('Uploaded file %s with mimeType %s' % (file_upload['title'], file_upload['mimeType']))
    except HttpError as error:
            print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
