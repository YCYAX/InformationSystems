"""
主页
"""
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QComboBox, QTableWidget, QPushButton, \
    QTableWidgetItem, QAbstractScrollArea, QHeaderView, QAbstractItemView
from mysqlDb.mysqlDb import MysqlDb
from box.messageBox import MessageBox


class Info(QWidget):
    """
    主页面
    """

    def __init__(self):
        super().__init__()
        """
        全局属性
        """
        self.state = False
        # 窗口高宽 1080 * 1920
        self.HIGH = int(1080 * 0.5)
        self.WIDTH = int(1920 * 0.5)
        # 数据库可读状态
        self.table_state = True
        # 数据库已读数据
        self.db_res = []
        # 姓名
        self.name = None
        self.age = None
        self.sex = None
        self.native = None
        self.peopleid = None
        self.home = None
        # 警号
        self.number = None
        # 工作
        self.work = None
        # 查询接口
        self.search = ''
        self.search_type = ''
        """
        加载类
        """
        self.db = MysqlDb()
        # 验证数据库
        try:
            self.db.connect()
        except:
            MessageBox.manualWarning("数据库错误", '数据库连接失败\n请检查数据库设置')
            self.table_state = False
        """
        加载逻辑
        """
        # 加载ui
        self.ui()

    def ui(self) -> None:
        """
        ui
        :return: None
        """
        """
        全局布局
        """
        # 主垂直布局
        self.main_vbox = QVBoxLayout()
        self.setLayout(self.main_vbox)
        # 按钮搜索框水平布局
        self.button_hbox = QHBoxLayout()
        self.main_vbox.addLayout(self.button_hbox)
        """
        窗口属性
        """
        # 大小
        self.resize(self.WIDTH, self.HIGH)
        # 标题
        self.setWindowTitle("警员信息管理系统")
        """
        功能
        """
        # 名字
        self.name_label = QLabel("姓名：")
        self.name_edit = QLineEdit("")
        self.name_edit.textChanged.connect(partial(self.textChanged, 'name'))
        self.button_hbox.addWidget(self.name_label)
        self.button_hbox.addWidget(self.name_edit)
        # 年龄
        self.age_label = QLabel("年龄：")
        self.age_edit = QLineEdit("")
        self.age_edit.textChanged.connect(partial(self.textChanged, 'age'))
        self.button_hbox.addWidget(self.age_label)
        self.button_hbox.addWidget(self.age_edit)
        # 性别
        self.sex_label = QLabel("性别：")
        self.sex_com = QComboBox()
        self.sex_com.addItems(['', '男', '女'])
        self.sex_com.currentIndexChanged[str].connect(partial(self.textChanged, 'sex'))
        self.button_hbox.addWidget(self.sex_label)
        self.button_hbox.addWidget(self.sex_com)
        # 籍贯
        self.native_label = QLabel("籍贯：")
        self.native_edit = QLineEdit("")
        self.native_edit.textChanged.connect(partial(self.textChanged, 'native'))
        self.button_hbox.addWidget(self.native_label)
        self.button_hbox.addWidget(self.native_edit)
        # 身份证号
        self.peopleid_label = QLabel("身份证号：")
        self.peopleid_edit = QLineEdit("")
        self.peopleid_edit.textChanged.connect(partial(self.textChanged, 'peopleid'))
        self.button_hbox.addWidget(self.peopleid_label)
        self.button_hbox.addWidget(self.peopleid_edit)
        # 家庭住址
        self.home_label = QLabel("家庭住址：")
        self.home_edit = QLineEdit("")
        self.home_edit.textChanged.connect(partial(self.textChanged, 'home'))
        self.button_hbox.addWidget(self.home_label)
        self.button_hbox.addWidget(self.home_edit)
        # 警号
        self.number_label = QLabel("警号：")
        self.number_edit = QLineEdit("")
        self.number_edit.textChanged.connect(partial(self.textChanged, 'number'))
        self.button_hbox.addWidget(self.number_label)
        self.button_hbox.addWidget(self.number_edit)
        # 工作岗位
        self.work_label = QLabel("工作岗位：")
        self.work_com = QComboBox()
        self.work_com.addItems(['', '户籍警', '治安警', '巡逻警', '社区警', '综合内勤警'])
        self.work_com.currentIndexChanged[str].connect(partial(self.textChanged, 'work'))
        self.button_hbox.addWidget(self.work_label)
        self.button_hbox.addWidget(self.work_com)
        # 确认
        self.sure_button = QPushButton("添加人员")
        self.sure_button.clicked.connect(self.addPersonal)
        self.button_hbox.addWidget(self.sure_button)
        # 查询功能
        self.search_label1 = QLabel("按照")
        self.search_com = QComboBox()
        self.search_com.addItems(['全部', '姓名', '年龄', '性别', '籍贯', '身份证号', '家庭住址', '警种', '警号'])
        self.search_com.currentIndexChanged[str].connect(partial(self.textChanged, 'search_type'))
        self.search_label2 = QLabel("检索：")
        self.search_edit = QLineEdit("")
        self.search_edit.textChanged.connect(partial(self.textChanged, 'search'))
        self.search_button = QPushButton("查询人员")
        self.search_button.clicked.connect(self.searchPersonal)
        # 删除功能
        self.del_button = QPushButton("删除人员")
        self.del_button.clicked.connect(self.deletePersonal)
        self.button_hbox.addWidget(self.search_label1)
        self.button_hbox.addWidget(self.search_com)
        self.button_hbox.addWidget(self.search_label2)
        self.button_hbox.addWidget(self.search_edit)
        self.button_hbox.addWidget(self.search_button)
        self.button_hbox.addWidget(self.del_button)
        # 修改功能
        self.change_button = QPushButton("修改人员")
        self.change_button.clicked.connect(self.changePersonal)
        self.button_hbox.addWidget(self.change_button)
        """
        人员数据表格
        """
        # 表格
        self.personal_table = QTableWidget()
        # 不可被编辑
        self.personal_table.setEditTriggers(QTableWidget.NoEditTriggers)
        # 宽度自适应
        self.personal_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置只能选中一行
        self.personal_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.main_vbox.addWidget(self.personal_table)
        # 初始化表格
        # 加载数据
        if self.table_state:
            self.db_res = self.db.readDB()
        # 行数 列数 表头
        self.personal_table.setColumnCount(8)
        self.personal_table.setRowCount(len(self.db_res))
        self.personal_table.setHorizontalHeaderLabels(
            ['姓名', '年龄', '性别', '籍贯', '身份证号', '家庭住址', '警种', '警号'])
        # 刷新列表
        self.refreshTable()

    def refreshTable(self) -> None:
        """
        刷新列表
        """
        # 读取库
        self.db_res = self.db.readDB()
        self.personal_table.setRowCount(len(self.db_res))
        for row in range(len(self.db_res)):
            # 添加数据 与 按钮
            self.personal_table.setItem(row, 0, QTableWidgetItem(f"{self.db_res[row][1]}"))
            self.personal_table.setItem(row, 1, QTableWidgetItem(f"{self.db_res[row][2]}"))
            self.personal_table.setItem(row, 2, QTableWidgetItem(f"{self.db_res[row][3]}"))
            self.personal_table.setItem(row, 3, QTableWidgetItem(f"{self.db_res[row][4]}"))
            self.personal_table.setItem(row, 4, QTableWidgetItem(f"{self.db_res[row][5]}"))
            self.personal_table.setItem(row, 5, QTableWidgetItem(f"{self.db_res[row][6]}"))
            self.personal_table.setItem(row, 6, QTableWidgetItem(f"{self.db_res[row][7]}"))
            self.personal_table.setItem(row, 7, QTableWidgetItem(f"{self.db_res[row][8]}"))

    def textChanged(self, textType: str, text: str) -> None:
        """
        edit输入变化
        :param textType: 框类型
        :param text: 输入内容
        """
        # 判断来源
        if textType == 'name':
            self.name = text
        elif textType == 'age':
            self.age = text
        elif textType == 'sex':
            self.sex = text
        elif textType == 'native':
            self.native = text
        elif textType == 'peopleid':
            self.peopleid = text
        elif textType == 'home':
            self.home = text
        elif textType == 'number':
            self.number = int(text)
        elif textType == 'work':
            self.work = text
        elif textType == 'search':
            self.search = text
        elif textType == 'search_type':
            if text == '全部':
                self.refreshTable()
            else:
                self.search_type = text

    def deletePersonal(self) -> None:
        """
        删除人员信息
        """
        # 获取行数
        selected_row = self.personal_table.currentRow()
        # 防止列表bug
        if selected_row >= 0:
            # 删除警告
            state = MessageBox.manualWarning(
                "删除警告", f'删除人员信息如下\n'
                            f'姓名:{self.db_res[selected_row][1]},年龄:{self.db_res[selected_row][2]},'
                            f'性别:{self.db_res[selected_row][3]},籍贯:{self.db_res[selected_row][4]},'
                            f'身份证号:{self.db_res[selected_row][5]},家庭住址:{self.db_res[selected_row][6]},'
                            f'警种:{self.db_res[selected_row][7]},警号:{self.db_res[selected_row][8]}')
            # 判断是否删除
            if state:
                self.personal_table.removeRow(selected_row)
                # 获取被删数据
                del_info = self.db_res[selected_row][-1]  # (6, '段岚', '人力资源部', '4985')
                # 删除数据集中的数据
                self.db_res.pop(selected_row)
                # 删除数据库中的数据
                self.db.delRecord(del_info)

    def addPersonal(self) -> None:
        """
        添加人员信息
        """
        # 防空
        if self.name and self.work and self.number and self.age and self.sex and self.native and self.peopleid and self.home != '':
            # 二次确认
            state = MessageBox.manualWarning(
                "添加确认", f'添加人员信息如下\n'
                            f'姓名:{self.name},年龄:{self.age},'
                            f'性别:{self.sex},籍贯:{self.native},'
                            f'身份证号:{self.peopleid},家庭住址:{self.home},'
                            f'警种:{self.work},警号:{self.number}')
            if state:
                # 添加信息
                self.db.addRecord(self.name, self.age, self.sex, self.native, self.peopleid, self.home, self.work,
                                  self.number)
                # 刷新库
                self.refreshTable()
        else:
            MessageBox.information('添加信息出错', "存在空输入，请检查", 2000)

    def searchPersonal(self):
        """
        查询人员
        """
        # 防空bug
        if self.search_type and self.search != '':
            # 查询数据
            res = self.db.searchRecord(**{
                self.search_type: self.search
            })
            # 清空表格
            self.personal_table.setRowCount(len(res))
            for row in range(len(res)):
                # 添加数据
                self.personal_table.setItem(row, 0, QTableWidgetItem(f"{res[row][1]}"))
                self.personal_table.setItem(row, 1, QTableWidgetItem(f"{res[row][2]}"))
                self.personal_table.setItem(row, 2, QTableWidgetItem(f"{res[row][3]}"))
                self.personal_table.setItem(row, 3, QTableWidgetItem(f"{res[row][4]}"))
                self.personal_table.setItem(row, 4, QTableWidgetItem(f"{res[row][5]}"))
                self.personal_table.setItem(row, 5, QTableWidgetItem(f"{res[row][6]}"))
                self.personal_table.setItem(row, 6, QTableWidgetItem(f"{res[row][7]}"))
                self.personal_table.setItem(row, 7, QTableWidgetItem(f"{res[row][8]}"))

        else:
            MessageBox.information('查询信息出错', "存在筛选或填写错误，请检查", 2000)

    def changePersonal(self) -> None:
        """
        修改记录
        """
        # 获取行数
        selected_row = self.personal_table.currentRow()
        if not self.state:
            # 防止列表bug
            if selected_row >= 0:
                # 直接填入数据
                res = self.db_res[selected_row]
                self.name_edit.setText(res[1])
                self.name = res[1]
                self.age_edit.setText(str(res[2]))
                self.age = res[2]
                self.sex_com.setCurrentText(res[3])
                self.sex = res[3]
                self.native_edit.setText(res[4])
                self.native = res[4]
                self.peopleid_edit.setText(res[5])
                self.peopleid = res[5]
                self.home_edit.setText(res[6])
                self.home = res[6]
                self.work_com.setCurrentText(res[7])
                self.work = res[7]
                self.number_edit.setText(str(res[8]))
                self.number = res[8]
                MessageBox.information("修改提示", '已读取数据', 1000)
                self.state = True
        else:
            res = self.db_res[selected_row]
            # 修改警告
            state = MessageBox.manualWarning(
                "修改警告", f'被修改人员原信息如下\n'
                            f'姓名:{res[1]},年龄:{res[2]},性别:{res[3]},籍贯:{res[4]},身份证号:{res[5]},'
                            f'家庭住址:{res[6]},警种:{res[7]},警号:{res[8]}'
                            f'\n被修改人员修改之后信息如下\n'
                            f'姓名:{self.name},年龄:{self.age},性别:{self.sex},籍贯:{self.native},'
                            f'身份证号:{self.peopleid},家庭住址:{self.home},警种:{self.work},警号:{self.number}')
            # 判断是否修改
            if state:
                # 修改数据集中的数据
                self.db.changeRecord(res[0], self.name, self.age, self.sex, self.native, self.peopleid,
                                     self.home, self.work, self.number)
                self.refreshTable()
                self.state = False

