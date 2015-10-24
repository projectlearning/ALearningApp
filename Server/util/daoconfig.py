import config

class DBConfig(config.Config):
	def __init__(self, filename):
		config.Config.__init__(self, filename)
		self.__ip = self.getItem("DataBase", "ip")
		self.__user = self.getItem("DataBase", "user")
		self.__passwd = self.getItem("DataBase", "passwd")
		self.__dbname = self.getItem("DataBase", "dbname")

	def getIp(self):
		return self.__ip

	def getUser(self):
		return self.__user

	def getPasswd(self):
		return self.__passwd

	def getDbname(self):
		return self.__dbname
