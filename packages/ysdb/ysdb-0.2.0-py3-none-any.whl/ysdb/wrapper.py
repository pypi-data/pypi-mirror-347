from ysdb.ysdbLib import RdbClient, PointRealData


class RdbWrapper:

    def __init__(self, host: str, port: int, user: str, password: str):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.rdbClient = RdbClient()
        self.token = None

        ret = self.rdbClient.connect(self.host, self.port)
        if ret != 1:
            raise Exception(f'YSDB connect failed {self.host}:{self.port}, {ret}')
        self.refresh_token()

    def disconnect(self):
        self.rdbClient.disconnect()

    def write_ctrl_data(self, mode: int, point_id: int, point_value):
        """
       写入遥控数据到YSDB
       :param mode: 0表示状态量，1表示模拟量
       :param point_id: 要遥控的测点id
       :param point_value: 要写入的遥控值。mode为0时，1代表打开，0代表关闭
       :return:
       """
        pointRealData = PointRealData(mode, point_id, 0, 0, point_value, 1, 0, 0)
        ret = self.rdbClient.writeCtrlDataById(0, 1, 0, self.token, pointRealData)
        return ret

    def refresh_token(self):
        """
        重新登录获取token（有效期10分钟）
        :return:
        """
        self.token = self.rdbClient.login(self.user, self.password)
        # 正常token示例：b'202cb962ac59075b964b07152d234b7000fea074fd7f0000699e03879a170000'
        if self.token == 'err' or self.token == '' or self.token == b'':  # 若用户名错则返回token为b''
            raise Exception(f'YSDB login failed {self.user}, {self.token}')
        # 将返回的token转为字符串，以便后面调用write_ctrl_data接口
        self.token = self.token.decode()
        return self.token
