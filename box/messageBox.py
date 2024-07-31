"""
消息类
"""
from PyQt5.QtWidgets import QMessageBox, QWidget


class MessageBox:
    """
    消息类
    """

    @classmethod
    def warning(cls, titleMessage: str, textMessage: str, animateTime: int) -> None:
        """
        警告消息 提供标题，文字，和自动消失时间
        :param titleMessage: 标题消息
        :param textMessage: 文字消息
        :param animateTime: 自动消失时间
        :return: None
        """
        # 创建box对象
        msgBox = QMessageBox()
        # 设置属性
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(textMessage)
        msgBox.setWindowTitle(titleMessage)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # 自动确认
        msgBox.button(QMessageBox.Ok).animateClick(animateTime)
        msgBox.exec()
        del msgBox

    @classmethod
    def information(cls, titleMessage: str, textMessage: str, animateTime: int) -> None:
        """
        提示消息 提供标题，文字，和自动消失时间
        :param titleMessage: 标题消息
        :param textMessage: 文字消息
        :param animateTime: 自动消失时间
        :return: None
        """
        # 创建box对象
        msgBox = QMessageBox()
        # 设置属性
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(textMessage)
        msgBox.setWindowTitle(titleMessage)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # 自动确认
        msgBox.button(QMessageBox.Ok).animateClick(animateTime)
        msgBox.exec()
        del msgBox

    @classmethod
    def manualWarning(cls, titleMessage: str, textMessage: str) -> bool:
        """
        手动警告消息 提供标题，文字，和自动消失时间
        :param titleMessage: 标题消息
        :param textMessage: 文字消息
        :return: bool
        """
        # 创建box对象
        msgBox = QMessageBox.question(QWidget(),
                                      titleMessage,
                                      textMessage,
                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                      QMessageBox.Cancel)
        # 判断如何操作
        if msgBox == QMessageBox.Yes:
            del msgBox
            return True
        elif msgBox == QMessageBox.No or QMessageBox.Cancel:
            del msgBox
            return False
