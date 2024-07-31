from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QHBoxLayout
from ui.Info import Info
from ui.Draw import Draw


class Index(QMainWindow):
    def __init__(self):
        super().__init__()
        """
        全局属性
        """
        # 窗口高宽 1080 * 1920
        self.HIGH = int(1080 * 0.5)
        self.WIDTH = int(1920 * 0.5)
        """
        窗口属性
        """
        # 大小
        self.resize(self.WIDTH, self.HIGH)
        # 标题
        self.setWindowTitle("警员信息管理系统")
        """
        全布局
        """
        # 创建一个 QWidget 作为中心窗口
        central_widget = QWidget()
        tmp = QWidget()
        self.setCentralWidget(central_widget)
        # 主页布局
        self.main_layout = QVBoxLayout(central_widget)
        # 按钮布局
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)
        # 窗口栈
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        # 页面
        self.draw = Draw()
        self.info = Info()
        # ui
        self.stacked_widget.addWidget(tmp)
        self.stacked_widget.setCurrentWidget(tmp)
        self.init_ui()

    def init_ui(self):
        # 结果可视化
        draw_page = QPushButton("数据统计")
        draw_page.clicked.connect(self.show_Info)
        self.button_layout.addWidget(draw_page)
        # 人员修改
        info_page = QPushButton("人员修改")
        info_page.clicked.connect(self.show_draw)
        self.button_layout.addWidget(info_page)
        # 页面修改
        self.stacked_widget.addWidget(self.draw)
        self.stacked_widget.addWidget(self.info)

    def show_Info(self):
        """
        人员检索
        """
        self.stacked_widget.setCurrentWidget(self.draw)

    def show_draw(self):
        """
        结果绘画
        """
        self.stacked_widget.setCurrentWidget(self.info)
