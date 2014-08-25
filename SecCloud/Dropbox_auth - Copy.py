# Include the Dropbox SDK
import dropbox
import pickle
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

pickle.dump( flow, open( "dropbox.p", "wb" ) )