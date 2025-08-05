import os

class Paths:
	@staticmethod
	def ensure_directories(file_path):
		directory = os.path.dirname(file_path)
		if directory:
			os.makedirs(directory, exist_ok=True)
