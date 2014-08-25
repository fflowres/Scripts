import unittest
import sys
import os
import time
import pickle

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
class GoogleAuthTest(unittest.TestCase):
  """Tests basic OAuth2 operations of auth.GoogleAuth."""

  def test_01_LocalWebserverAuthWithClientConfigFromFile(self):

    # Test if authentication works with config read from file
    packageName = "test.z.crypt"
    foldername = "SeccuDB"
    ga = GoogleAuth('settings/test1.yaml')
    #ga.getAuthURL()
    try:
      ga.LoadClientConfig()
      ga.LoadCredentials()
      ga.Authorize()
    except:

      print ga.GetAuthUrl()
      code = raw_input("code: ").strip()

      ga.Auth(code)
      ga.SaveCredentials()

    print "complete Auth"
    drive = GoogleDrive(ga)
    #flist = drive.ListFile({'q': "title contains '.crypt' and trashed = false"})
    folderlistquery = drive.ListFile({'q': "title = 'SeccuDB' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"})
    

    cloudfolder = folderlistquery.GetList()
    if (len(cloudfolder) == 0):
      #create folder 
      
      folder = drive.CreateFile()
      folder['title'] = "SeccuDB"
      folder['mimeType'] = "application/vnd.google-apps.folder"
      folder['parents'] = "root"
      folder.Upload()
      cloudfolder = folderlistquery.GetList()
      if (len(cloudfolder) == 0):
        print "error"
        raise error('GooglePermissionsError')


    cloudfolderid = cloudfolder[0]['id']
    print cloudfolderid

    databaseListquery = drive.ListFile({'q': "'%s' in parents and trashed = false" % (cloudfolderid)})
    databaseList = databaseListquery.GetList()


    database_file = drive.CreateFile()
    database_file['title'] = packageName
    database_file['parents']=[{"kind": "drive#fileLink" ,'id': str(cloudfolderid) }]
    #check if already exists, if so, get id and update
    databasenamelist = []
    for databaseAvaliable in databaseList:
      databasenamelist.append(databaseAvaliable['title'])
    if packageName in databasenamelist:
      cloudPackageQuery = drive.ListFile({'q': "title = '%s' and trashed = false" % (packageName)})
      cloudPackage = cloudPackageQuery.GetList()

      if(len(cloudPackage) > 1): # if theres more than one, go for the most recent
        packdates = []
        for everypack in cloudPackage:
          packdates.append((everypack['modifiedByMeDate'],everypack['id']))
        database_file['id'] = sorted(packdates,reverse=True)[0][1]

      else:
        database_file['id'] = cloudPackage[0]['id']


    database_file.Upload()
    
    #folderid = folders[0]["id"]
    # databaseListquery = drive.ListFile({'q': "title contains 'z.crypt' and trashed = false"})








  


if __name__ == '__main__':
  unittest.main()
