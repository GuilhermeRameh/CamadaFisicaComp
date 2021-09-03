from math import ceil

class FileManager:
	def __init__(self, filepath):
		self.filepath = filepath
		self.extension = self.filepath.split(".")[1]
	def dividePackages(self):
		packageList = []
		with open(self.filepath, "rb") as file:
			binaryFile = file.read()
			binaryFile = bytearray(binaryFile)
			for i in range(0, int(ceil(len(binaryFile)/114))):
				packageList.append(binaryFile[:144])
				del(binaryFile[:144])
			return packageList
	def returnExtension(self):
		if len(bytes(self.extension, encoding="utf-8")):
			return bytes(self.extension, encoding="utf-8")
		extensionBytes = bytes(self.extension, encoding="utf-8") + b'\x00'
		return extensionBytes
