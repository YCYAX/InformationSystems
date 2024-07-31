"""
数据库交互
"""
import mysql.connector


class MysqlDb:
    """
    数据库类
    """

    def __init__(self):
        # 必要字段
        self.host = 'localhost'
        self.user = 'root'
        self.password = '123456'
        self.database = 'police_information'

    def connect(self) -> None:
        """
        链接数据库
        :return: None
        """
        # 创建db对象
        mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        # 创建游标对象
        cursor = mydb.cursor()
        # 关闭游标和数据库连接
        cursor.close()
        mydb.close()

    def readDB(self) -> list:
        """
        数据查询
        :return: 数据列表
        """
        # 创建db对象
        mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        # 创建游标对象
        cursor = mydb.cursor()
        # 查询数据
        cursor.execute("SELECT * FROM personal")
        # 读取查询结果
        result = cursor.fetchall()
        # 关闭游标和数据库连接
        cursor.close()
        mydb.close()
        return result

    def delRecord(self, number: str):
        """
        删除一条记录
        :param number: 警号
        """
        # 创建db对象
        mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        # 创建游标对象
        cursor = mydb.cursor()
        # 删除数据
        cursor.execute(f"DELETE FROM personal WHERE number = {str(number)}")
        # 关闭游标和数据库连接
        cursor.close()
        mydb.close()

    def addRecord(self, *args):
        """
        添加一条记录
        """
        # 创建db对象
        mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        # 创建游标对象
        cursor = mydb.cursor()
        # 添加数据
        cursor.execute(f"INSERT INTO personal (name,age,sex,native,peopleid,home,work,number) VALUES ("
                       f"'{args[0]}',{args[1]},'{args[2]}','{args[3]}','{args[4]}','{args[5]}','{args[6]}',{args[7]})")
        # 关闭游标和数据库连接
        cursor.close()
        mydb.close()

    def searchRecord(self, **kwargs) -> list:
        """
        查询一条记录
        :param kwargs: 关键字
        :return: list 结果
        """
        # 获取key和value
        key = list(kwargs.keys())[0]
        value = list(kwargs.values())[0]
        # 确定列
        if key == '姓名':
            key = 'name'
        elif key == '年龄':
            key = 'age'
        elif key == '性别':
            key = 'sex'
        elif key == '籍贯':
            key = 'native'
        elif key == '身份证号':
            key = 'peopleid'
        elif key == '家庭住址':
            key = 'home'
        elif key == '警种':
            key = 'work'
        elif key == '警号':
            key = 'number'
        # 创建db对象
        mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        # 创建游标对象
        cursor = mydb.cursor()
        # 查询数据
        cursor.execute(f"SELECT * FROM personal WHERE {key} LIKE '%{value}%'")
        # 读取查询结果
        result = cursor.fetchall()
        # 关闭游标和数据库连接
        cursor.close()
        mydb.close()
        return result

    def changeRecord(self, *args):
        """
        修改一条记录
        """
        # 创建db对象
        mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        # 创建游标对象
        cursor = mydb.cursor()
        # 添加数据
        cursor.execute(f"UPDATE personal SET name = '{args[1]}',age = {args[2]},sex = '{args[3]}',native = '{args[4]}',"
                        f"peopleid = '{args[5]}',home = '{args[6]}',work = '{args[7]}',number = {args[8]} "
                       f"WHERE id = {args[0]}")
        # 关闭游标和数据库连接
        cursor.close()
        mydb.close()