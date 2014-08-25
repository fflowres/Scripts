# Include the Dropbox SDK
import dropbox

# Get your app key and secret from the Dropbox developer website
app_key = 'p2iu4n7f9yegl3u'
app_secret = '0903whnau7p2zde'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

authorize_url = flow.start()

authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()

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