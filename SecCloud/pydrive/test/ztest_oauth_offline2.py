import unittest
import sys
import os
import time
import pickle

from pydrive.auth import GoogleAuth

class GoogleAuthTest(unittest.TestCase):
  """Tests basic OAuth2 operations of auth.GoogleAuth."""

  def test_01_LocalWebserverAuthWithClientConfigFromFile(self):

    # Test if authentication works with config read from file
    ga = GoogleAuth('settings/test1.yaml')
    code = raw_input("code: ").strip()
    ga.CommandLineAuth(code)
    pickle.dump( ga, open( "auth.p", "wb" ) )
    authCode = raw_input("enter code: ")
    self.assertEqual(ga.access_token_expired, False)
    # Test if correct credentials file is created
    self.CheckCredentialsFile('credentials/1.dat')
    time.sleep(1)

  


if __name__ == '__main__':
  unittest.main()
