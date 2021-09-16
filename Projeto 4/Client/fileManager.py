from math import ceil

class FileManager:
	def __init__(self, filepath):
		self.filepath = str(filepath)
		self.extension = self.filepath.split(".")[1]
	def dividePackages(self):
		packageList = []
		byteFilename = bytes(self.filepath, 'utf-8')
		packageList.append(byteFilename)
		with open(self.filepath, "rb") as file:
			binaryFile = file.read()
			binaryFile = bytearray(binaryFile)
			for i in range(0, int(ceil(len(binaryFile)/114))):
				packageList.append(binaryFile[:114])
				del(binaryFile[:114])
			return packageList

# if __name__ == '__main__':
# 	print("hello")
# 	Fm = FileManager("test.txt")
# 	print(Fm.dividePackages())
# 	print(Fm.returnExtension())