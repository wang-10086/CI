import sys
from device_data import Signal, Switch, Track, Button
from route import Route
from read_files import readInterlockTable, read_tracks, read_signals, read_joints, read_buttons
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont, QPalette
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QPushButton, QMessageBox, QInputDialog, QLineEdit, QVBoxLayout, QTextEdit, QLabel


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

        self.textEdit = QTextEdit(self) # 创建文本框
        self.textEdit.setStyleSheet("QTextEdit { color: black;background-color: lightgrey; }")
        self.textEdit.setGeometry(QtCore.QRect(1080, 580, 400, 300))
        self.textEdit.setReadOnly(True)  # 设置为只读，防止用户编辑

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


class MainWindow(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        interlock_table_path = '联锁表.xlsx'
        signal_data_path = 'signal_data.txt'
        track_data_path = 'track_data.txt'
        joint_data_path = 'joint_data.txt'
        button_data_path = 'button_data.txt'

        # 读取设备数据
        self.tracks = read_tracks(track_data_path)  # 轨道区段
        self.joints = read_joints(joint_data_path)  # 绝缘节
        self.buttons = read_buttons(button_data_path)  # 信号机按钮
        self.signals = read_signals(signal_data_path)  # 信号机

        # 读取联锁表
        self.interlockTable = readInterlockTable(interlock_table_path)

        # 创建按钮
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

        # # 打印初始化的信号机、道岔和轨道区段信息
        # print("信号机:")
        # for signal in self.signals:
        #     print(f"信号机编号: {signal.SignalID}, 点灯状态: {signal.SignalStatus}, 征用状态: {signal.UsedFlag}")
        #
        # print("道岔:")
        # for switch in self.switches:
        #     print(f"道岔编号: {switch.SwitchID}, 状态: {switch.SwitchStatus}, 征用状态: {switch.UsedFlag}")
        #
        # print("轨道区段:") for track in self.tracks: print( f"区段编号: {track.TrackID}, 状态: {track.TrackStatus},
        # 征用状态: {track.UsedFlag}, 起点坐标: {track.start_point}, 终点坐标: {track.end_point}")

        # # 打印联锁表信息
        # print('联锁表信息:')
        # for route in self.interlockTable:
        #     route.display_route_info()

    # 区段线条绘制
    def paintEvent(self, event):
        painter = QPainter(self)
        linecolor = QColor(255, 255, 255)
        linewidth = 3

        # 绘制区段
        for track in self.tracks:
            pen = QPen(linecolor, linewidth, Qt.SolidLine)  # 红色线条，宽度为3
            painter.setPen(pen)
            start_point = QPoint(track.start_point[0], track.start_point[1])
            end_point = QPoint(track.end_point[0], track.end_point[1])
            painter.drawLine(start_point, end_point)
            # 计算线条中点
            mid_x = (track.start_point[0] + track.end_point[0]) // 2
            mid_y = track.end_point[1]

            # 绘制线条名称
            painter.setPen(QColor(255, 255, 255))  # 设置文字颜色为白色
            painter.drawText(mid_x, mid_y, track.TrackID)  # 在中点绘制线条名称

        # 绘制绝缘节等
        for joint in self.joints:
            pen = QPen(linecolor, linewidth, Qt.SolidLine)  # 红色线条，宽度为3
            painter.setPen(pen)
            start_point = QPoint(joint.start_point[0], joint.start_point[1])
            end_point = QPoint(joint.end_point[0], joint.end_point[1])
            painter.drawLine(start_point, end_point)

        # 绘制按钮
        for button in self.buttons:
            btn = QPushButton(self)
            btn.move(*button.point)
            btn.setStyleSheet("QPushButton { background-color: rgb(192, 192, 192); }")
            btn.setFixedSize(21, 21)
            btn.show()
            btn.clicked.connect(lambda checked, name=button.ButtonID: self.onButtonClick(name))

        # 绘制信号机
        for signal in self.signals:
            pen = QPen(linecolor, linewidth, Qt.SolidLine)
            painter.setPen(pen)
            painter.setBrush(QBrush(QColor(255, 0, 0)))  # 使用红色填充
            center_point = QPoint(signal.point[0], signal.point[1])
            radius = 10  # 圆形的半径
            painter.drawEllipse(center_point, radius, radius)

    def update_ui(self):
        """
        更新界面控件参数
        """
        pass

    def onButtonClick(self, name):
        """点击信号机按钮 """
        self.addMessage(f"Button {name} clicked")

    def on_zongrenjie_click(self):
        """总人解按钮点击事件"""
        password, ok = QInputDialog.getText(self, "密码输入", "请输入密码:", QLineEdit.Password)

        if ok and password == "1234":  # 将 "正确密码" 替换为你实际使用的密码
            self.textEdit.append("密码正确，进行下一步操作")
            QMessageBox.information(self, "信息", "密码正确，进行下一步操作")

            self.addMessage("总人解")

        else:
            self.textEdit.append("密码错误")
            QMessageBox.warning(self, "警告", "密码错误")

    def on_zongquxiao_click(self):
        """总取消按钮点击事件"""
        password, ok = QInputDialog.getText(self, "密码输入", "请输入密码:", QLineEdit.Password)

        if ok and password == "1234":  # 将 "正确密码" 替换为你实际使用的密码
            self.textEdit.append("密码正确，进行下一步操作")
            QMessageBox.information(self, "信息", "密码正确，进行下一步操作")

            self.addMessage("总取消")

        else:
            self.textEdit.append("密码错误")
            QMessageBox.warning(self, "警告", "密码错误")

    def on_zongdingwei_click(self):
        """总定位按钮点击事件"""
        self.addMessage("总定位")
        for switch in self.switches:
            switch.SwitchStatus = 0

    def on_zongfanwei_click(self):
        """总反位按钮点击事件"""
        self.addMessage("总反位")
        for switch in self.switches:
            switch.SwitchStatus = 1

    def on_run_click(self):
        """模拟行车按钮点击事件"""
        self.addMessage("模拟行车按钮点击")

    def on_dansuo_click(self):
        """
        单锁:将选中道岔状态设为锁闭
        """
        for switch in self.switches:
            switch.LockFlag = 1

    def on_danjie_click(self):
        """
        单解:将选中道岔状态设为开
        """
        for switch in self.switches:
            switch.LockFlag = 0

    def zongdingwei(self):
        """
        总定位:将所有道岔状态设为定位0
        """
        for switch in self.switches:
            switch.SwitchStatus = 0

    def zongfanwei(self):
        """
        总反位:将所有道岔状态设为反位1
        """
        for switch in self.switches:
            switch.SwitchStatus = 1

    def dansuo(self):
        """
        单锁:将所有道岔状态设为锁闭
        """
        # 遍历所有道岔按钮，找出被选中的那一个
        for switch in self.switches:
            if switch.SelectedFlag == 1:
                switch.LockFlag = 1

    def route_selection(self, route_id):
        """
        进路选排函数
        """
        print("执行进路选排")
        # 确认进路是否可用
        signal_id = self.interlockTable[route_id - 1].SignalID
        # 判断信号机是否被征用
        for signal in self.signals:
            if signal.SignalID == signal_id:
                if signal.UsedFlag == 1:
                    print(f"信号机{signal.SignalID}已被征用，无法选排")
                    return
        # 判断区段是否空闲
        track_ids = self.interlockTable[route_id - 1].TrackID
        for tarck_id in track_ids:
            for track in self.tracks:
                if track.TrackID == tarck_id:
                    if track.TrackStatus == 1:
                        print(f"区段{track.TrackID}已被占用，无法选排")
                        return
        # 判断区段是否被征用
        track_ids = self.interlockTable[route_id - 1].TrackID
        for track_id in track_ids:
            for track in self.tracks:
                if track.TrackID == track_id:
                    if track.UsedFlag == 1:
                        print(f"区段{track.TrackID}已被征用，无法选排")
                        return
        # 判断道岔是否被征用
        switch_ids = self.interlockTable[route_id - 1].SwitchID
        for switch_id in switch_ids:
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.UsedFlag == 1:
                        print(f"道岔{switch.SwitchID}被征用，无法选排")
                        return
        # 判断敌对信号是否开放
        opposing_signals = self.interlockTable[route_id - 1].OpposingSignal
        for opposing_signal in opposing_signals:
            for signal in self.signals:
                if signal.SignalID == opposing_signal:
                    if signal.SignalStatus == 1:
                        print(f"敌对信号{signal.SignalID}开放，无法选排")
                        return
        # 判断区段是否被锁闭
        track_ids = self.interlockTable[route_id - 1].TrackID
        for track_id in track_ids:
            for track in self.tracks:
                if track.TrackID == track_id:
                    if track.LockFlag == 1:
                        print(f"区段{track.TrackID}已被锁闭，无法选排")
                        return
        # 判断照查条件
        # 判断道岔是否锁闭
        switch_ids = self.interlockTable[route_id - 1].SwitchID
        for switch_id in switch_ids:
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.LockFlag == 1:
                        print(f"道岔{switch.SwitchID}被锁闭，无法选排")
                        return
        # 判断道岔是否被封锁
        switch_ids = self.interlockTable[route_id - 1].SwitchID
        for switch_id in switch_ids:
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.FuncLockFlag == 1:
                        print(f"道岔{switch.SwitchID}被封锁，无法选排")
                        return
        # 征用道岔、区段、信号机







    def route_lock(self):
        """
        进路锁闭函数
        """
        print("执行进路锁闭")

    def signal_open(self):
        """
        信号开放函数
        """
        print("执行信号开放")

    def signal_hold_open(self):
        """
        信号开放保持函数
        """
        print("执行信号开放保持")

    def route_normal_unlock(self):
        """
        进路正常解锁函数
        """
        print("执行进路正常解锁")

    def route_cancel(self):
        """
        进路取消函数
        """
        print("执行进路取消")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
