from ysdb.ysdbLib import RdbClient

rdbClient = RdbClient()


class RdbWrapper:

	def connect(self, ip, port):
		return rdbClient.connect(ip, port)


	def disconnect(self):
		rdbClient.disconnect()


	def write_ctrl_data(self):
		rdbClient.writeCtrlDataById()
		print()