import argon2



class HashFeature:

	@staticmethod
	def encript(passwd: str) -> str:
		""""""
		hash = argon2.PasswordHasher().hash(passwd)
		return hash

	@staticmethod
	def verify(passwd: str, encripted_passwd: str) -> bool:
		""""""
		try:
			argon2.PasswordHasher().verify(encripted_passwd, passwd)
			return True
		except argon2.exceptions.VerifyMismatchError:
			return False


