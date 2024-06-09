from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QTextEdit, QLabel


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1500, 900)
        self.setPalette(QPalette(QColor(0, 0, 0)))

        self.label1 = QLabel(Form)
        self.label1.setGeometry(50, 250, 300, 50)  # 设置文本标签的位置和大小
        self.label1.setStyleSheet("color: white;")  # 设置文本颜色
        self.label1.setText("北京方面")  # 设置文本内容
        font = QFont()
        font.setPointSize(15)  # 设置字体大小
        self.label1.setFont(font)

        self.label2 = QLabel(Form)
        self.label2.setGeometry(1350, 250, 300, 50)  # 设置文本标签的位置和大小
        self.label2.setStyleSheet("color: white;")  # 设置文本颜色
        self.label2.setText("广州方面")  # 设置文本内容
        self.label2.setFont(font)

        self.label3 = QLabel(Form)
        self.label3.setGeometry(1080, 540, 300, 50)  # 设置文本标签的位置和大小
        self.label3.setStyleSheet("color: white;")  # 设置文本颜色
        self.label3.setText("信息提示窗")  # 设置文本内容
        self.label3.setFont(font)

        self.textEdit = QTextEdit(self)  # 创建文本框
        self.textEdit.setStyleSheet("QTextEdit { color: black;background-color: lightgrey; }")
        self.textEdit.setGeometry(QtCore.QRect(1080, 580, 400, 300))
        self.textEdit.setReadOnly(True)  # 设置为只读，防止用户编辑

        # 创建功能按钮
        self.button1 = QPushButton("总人解", self)
        self.button1.setGeometry(50, 850, 100, 40)  # 设置按钮的位置和大小
        self.button1.setStyleSheet("QPushButton { color: black; background-color:lightgrey; }")
        self.button1.clicked.connect(self.on_zongrenjie_click)  # 绑定事件

        self.button2 = QPushButton("总取消", self)
        self.button2.setGeometry(150, 850, 100, 40)  # 设置按钮的位置和大小
        self.button2.setStyleSheet("QPushButton { color: black; background-color:lightgrey; }")
        self.button2.clicked.connect(self.on_zongquxiao_click)

        self.button3 = QPushButton("总定位", self)
        self.button3.setGeometry(250, 850, 100, 40)  # 设置按钮的位置和大小
        self.button3.setStyleSheet("QPushButton { color: black; background-color:lightgrey; }")
        self.button3.clicked.connect(self.on_zongdingwei_click)

        self.button4 = QPushButton("总反位", self)
        self.button4.setGeometry(350, 850, 100, 40)
        self.button4.setStyleSheet("QPushButton { color: black; background-color:lightgrey; }")
        self.button4.clicked.connect(self.on_zongfanwei_click)

        self.button5 = QPushButton("单锁", self)
        self.button5.setGeometry(450, 850, 100, 40)
        self.button5.setStyleSheet("QPushButton { color: black; background-color:lightgrey; }")
        self.button5.clicked.connect(self.on_dansuo_click)

        self.button6 = QPushButton("单解", self)
        self.button6.setGeometry(550, 850, 100, 40)
        self.button6.setStyleSheet("QPushButton { color: black; background-color:lightgrey; }")
        self.button6.clicked.connect(self.on_danjie_click)

        self.button7 = QPushButton("模拟行车", self)
        self.button7.setGeometry(650, 850, 100, 40)
        self.button7.setStyleSheet("QPushButton { color: black; background-color:lightgrey; }")
        self.button7.clicked.connect(self.on_run_click)

        # 添加文本框到布局中
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def addMessage(self, message):
        """向文本框中添加新信息"""
        self.textEdit.append(message)