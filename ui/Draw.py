from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from mysqlDb.mysqlDb import MysqlDb

from pylab import mpl

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]


class Draw(QWidget):
    def __init__(self):
        super().__init__()
        """
        加载类
        """
        self.db = MysqlDb()
        self.init_ui()

    def init_ui(self):
        # 创建一个 Matplotlib 图形
        self.figure = plt.figure()

        # 创建第一个饼图
        ax1 = self.figure.add_subplot(131)
        # 初始年龄
        number = 18
        # 数据
        check = [(18, 25), (26, 35), (36, 40), (41, 50)]
        data1 = []
        # 循环读取
        for i in check:
            tmp = 0
            while i[0] <= number <= i[1]:
                add = self.db.searchRecord(**{"年龄": number})
                number += 1
                tmp += len(add)
            data1.append(tmp)
        labels1 = ['18-25', '26-35', '36-40', '41-50']
        ax1.pie(data1, labels=labels1, autopct='%1.1f%%')
        ax1.set_title('年龄比例')

        # 创建第二个饼图
        ax2 = self.figure.add_subplot(132)
        data2 = [len(self.db.searchRecord(**{"性别": '男'})), len(self.db.searchRecord(**{"性别": '女'}))]
        labels2 = ['男', '女']
        ax2.pie(data2, labels=labels2, autopct='%1.1f%%')
        ax2.set_title('男女比例')

        # 创建第三个饼图
        ax3 = self.figure.add_subplot(133)
        labels3 = ['户籍警', '治安警', '巡逻警', '社区警', '综合内勤警']
        data3 = [len(self.db.searchRecord(**{"警种": i})) for i in labels3]
        ax3.pie(data3, labels=labels3, autopct='%1.1f%%')
        ax3.set_title('警种比例')

        # 创建一个 Matplotlib 画布
        self.canvas = FigureCanvas(self.figure)

        # 创建一个布局
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
