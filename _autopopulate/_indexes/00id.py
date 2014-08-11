# id
# EncUniqueHashIndex

# inserted automatically
import os
import marshal

import struct
import shutil

from hashlib import md5

# custom db code start
# db_custom


# custom index code start
# ind_custom

from _dbindex import Salsa20Storage
from hashlib import sha256

# source of classes in index.classes_code
# classes_code


# index code start

class EncUniqueHashIndex(UniqueHashIndex):

	__enc_key = 'a' * 32

	custom_header = """
from _dbindex import Salsa20Storage
from hashlib import sha256"""

	def __init__(self, *args, **kwargs):
		super(EncUniqueHashIndex, self).__init__(*args, **kwargs)

	@property
	def enc_key(self):
		return self.__enc_key

	@enc_key.setter
	def enc_key(self, value):
		if len(value) != 32:
			self.__enc_key = sha256(value).digest()
		else:
			self.__enc_key = value
		self.storage.enc_key = self.__enc_key

	def _setup_storage(self):
		if not self.storage:
			self.storage = Salsa20Storage(
				self.db_path, self.name, self.enc_key)

	def _open_storage(self):
		self._setup_storage()
		self.storage.open()

	def _create_storage(self):
		self._setup_storage()
		self.storage.create()
