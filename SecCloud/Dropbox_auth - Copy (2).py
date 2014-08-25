# Include the Dropbox SDK
import dropbox
import pickle

flow = pickle.load( open( "dropbox.p", "rb" ) )
code = raw_input("enter code")
access_token, user_id = flow.finish(code)


client = dropbox.client.DropboxClient(access_token)
print 'linked account: ', client.account_info()

#Uploading files
f = open('test.jpg', 'rb')
response = client.put_file('/test.jpg', f)
print "uploaded:", response


#Listing folders
folder_metadata = client.metadata('/')
print "metadata:", folder_metadata


#Downloading files

f, metadata = client.get_file_and_metadata('/test.jpg')
out = open('test-downloaded.jpg', 'wb')
out.write(f.read())
out.close()
print metadata