import sys
from device_data import Signal, Switch, Track, Button
from ui_data import SwitchButton
from route import Route
from read_files import readInterlockTable, read_tracks, read_signals, read_joints, read_buttons, read_switches
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

        self.textEdit = QTextEdit(self)  # 创建文本框
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
        self.is_painted = False
        interlock_table_path = '联锁表.xlsx'
        signal_data_path = 'signal_data.txt'
        track_data_path = 'track_data.txt'
        joint_data_path = 'joint_data.txt'
        button_data_path = 'button_data.txt'
        switch_data_path = 'switch_data.txt'

        # 读取设备数据
        self.tracks = read_tracks(track_data_path)  # 轨道区段
        self.joints = read_joints(joint_data_path)  # 绝缘节
        self.buttons = read_buttons(button_data_path)  # 信号机按钮
        self.signals = read_signals(signal_data_path)  # 信号机
        self.switches = read_switches(switch_data_path)  # 道岔

        # 读取联锁表
        self.interlockTable = readInterlockTable(interlock_table_path)

        # 绘制信号机按钮
        for button in self.buttons:
            btn = QPushButton(self)
            btn.move(*button.point)
            btn.setStyleSheet("QPushButton { background-color: rgb(192, 192, 192); }")
            btn.setFixedSize(21, 21)
            # btn.clicked.connect(lambda checked, name=button.ButtonID: self.onButtonClick(name))

        # 绘制道岔按钮
        self.switch_btns = []
        for switch in self.switches:
            # 计算线条中点
            x = switch.start_point[0]
            y = switch.end_point[1] + 5
            # 绘制道岔按钮
            switch_btn = SwitchButton(switch.SwitchID, switch.SwitchID, self)
            switch_btn.point = [x, y]
            switch_btn.move(*switch_btn.point)
            switch_btn.setStyleSheet("QPushButton { color: white; background-color:black; }")
            switch_btn.setFixedSize(20, 20)
            self.switch_btns.append(switch_btn)
            # switch_btn.clicked.connect(lambda checked, name=switch.SwitchID: self.onSwitchClick(name))

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

        self.button8 = QPushButton("办理进路", self)
        self.button8.setGeometry(750, 850, 100, 40)
        self.button8.setStyleSheet("QPushButton { color: black; background-color:lightgrey; }")
        self.button8.clicked.connect(self.route_process_click)

        # # 打印初始化的信号机、道岔和轨道区段信息
        # print("信号机:")
        # for signal in self.signals:
        #     print(f"信号机编号: {signal.SignalID}, 点灯状态: {signal.SignalStatus}, 征用状态: {signal.UsedFlag}")
        #
        # print("道岔:")
        # for switch in self.switches:
        #     print(f"道岔编号: {switch.SwitchID}, 状态: {switch.SwitchStatus}, 征用状态: {switch.UsedFlag}")
        #
        # print("轨道区段:")
        # for track in self.tracks: print(
        #     f"区段编号: {track.TrackID}, 状态: {track.TrackStatus},征用状态: {track.UsedFlag}, "
        #     f"起点坐标: {track.start_point}, 终点坐标: {track.end_point}")
        #
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
            start_point = QPoint(track.start_point[0], track.start_point[1])
            end_point = QPoint(track.end_point[0], track.end_point[1])
            if track.LockFlag == 0:
                pen = QPen(QColor(0, 0, 255), linewidth, Qt.SolidLine)  # 未锁闭显示蓝色
            else:
                pen = QPen(QColor(224, 224, 224), linewidth, Qt.SolidLine)  # 锁闭显示灰白色

            if track.TrackStatus == 1:
                pen = QPen(QColor(255, 0, 0), linewidth, Qt.SolidLine)  # 占用显示红色

            painter.setPen(pen)
            painter.drawLine(start_point, end_point)

            # 计算线条中点
            mid_x = (track.start_point[0] + track.end_point[0]) // 2
            mid_y = track.end_point[1] - 5

            # 绘制线条名称
            painter.setPen(QColor(255, 255, 255))  # 设置文字颜色为白色
            painter.drawText(mid_x, mid_y, track.TrackID)  # 在中点绘制线条名称

        # 绘制绝缘节等
        for joint in self.joints:
            pen = QPen(linecolor, linewidth, Qt.SolidLine)  # 白色线条，宽度为3
            painter.setPen(pen)
            start_point = QPoint(joint.start_point[0], joint.start_point[1])
            end_point = QPoint(joint.end_point[0], joint.end_point[1])
            painter.drawLine(start_point, end_point)

        # 绘制信号机
        for signal in self.signals:
            pen = QPen(linecolor, linewidth, Qt.SolidLine)
            painter.setPen(pen)
            painter.setBrush(QBrush(QColor(255, 0, 0)))  # 使用红色填充
            center_point = QPoint(signal.point[0], signal.point[1])
            radius = 10  # 圆形的半径
            painter.drawEllipse(center_point, radius, radius)

        # 绘制道岔
        for switch in self.switches:
            if switch.SwitchStatus == 0:
                pen = QPen(QColor(0, 255, 0), linewidth, Qt.SolidLine)  # 定位显示绿色
            else:
                pen = QPen(QColor(0, 0, 255), linewidth, Qt.SolidLine)  # 反位显示蓝色
            painter.setPen(pen)
            start_point = QPoint(switch.start_point[0], switch.start_point[1])
            end_point = QPoint(switch.end_point[0], switch.end_point[1])
            painter.drawLine(start_point, end_point)

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
        self.update()

    def on_zongfanwei_click(self):
        """总反位按钮点击事件"""
        self.addMessage("总反位")
        for switch in self.switches:
            switch.SwitchStatus = 1
        self.update()

    def on_run_click(self):
        """模拟行车按钮点击事件"""
        self.addMessage("模拟行车按钮点击")

    def on_dansuo_click(self):
        """
        单锁:将选中道岔状态设为锁闭
        """
        for switch_btn in self.switch_btns:
            if switch_btn.is_selected:
                switch_id = switch_btn.switchID
                for switch in self.switches:
                    if switch.SwitchID == switch_id:
                        switch.LockFlag = 1
                        # 按钮停止闪烁，并取消按钮选中状态
                        switch_btn.stop_blinking()
                        switch_btn.is_selected = False
                        self.addMessage(f"道岔{switch.SwitchID}被锁闭")

        self.update()

    def on_danjie_click(self):
        """
        单解:将选中道岔状态解锁
        """
        for switch_btn in self.switch_btns:
            if switch_btn.is_selected:
                switch_id = switch_btn.switchID
                for switch in self.switches:
                    if switch.SwitchID == switch_id:
                        switch.LockFlag = 0
                        # 按钮停止闪烁，并取消按钮选中状态
                        switch_btn.stop_blinking()
                        switch_btn.is_selected = False
                        self.addMessage(f"道岔{switch.SwitchID}已解锁")

        self.update()

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

    def route_process_click(self):
        """
        办理进路按钮点击事件
        """
        # 弹出输入框，输入进路编号
        # 获取联锁表进路总数
        route_number = len(self.interlockTable)
        route_id, ok = QInputDialog.getInt(self, "进路办理", "请输入进路编号:", 1, 1, route_number)
        if ok:
            self.addMessage(f"办理进路{route_id}")
            self.route_selection(route_id)
            self.route_lock(route_id)
            self.signal_open(route_id)
            self.update()
            print("办理进路成功")

    def route_selection(self, route_id):
        """
        进路选排函数
        """
        print("执行进路选排")
        signal_id = self.interlockTable[route_id - 1].signal_name
        track_ids = self.interlockTable[route_id - 1].track_sections
        switch_ids = self.interlockTable[route_id - 1].switches
        opposing_signals = self.interlockTable[route_id - 1].opposing_signals

        # 判断信号机是否被征用
        for signal in self.signals:
            if signal.SignalID == signal_id:
                if signal.UsedFlag == 1:
                    print(f"信号机{signal.SignalID}已被征用，无法选排")
                    return
        # 判断区段是否空闲
        for tarck_id in track_ids:
            for track in self.tracks:
                if track.TrackID == tarck_id:
                    if track.TrackStatus == 1:
                        print(f"区段{track.TrackID}已被占用，无法选排")
                        return
        # 判断区段是否被征用
        for track_id in track_ids:
            for track in self.tracks:
                if track.TrackID == track_id:
                    if track.UsedFlag == 1:
                        print(f"区段{track.TrackID}已被征用，无法选排")
                        return
        # 判断道岔是否被征用
        for switch_id in switch_ids.keys():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.UsedFlag == 1:
                        print(f"道岔{switch.SwitchID}被征用，无法选排")
                        return
        # 判断敌对信号是否开放
        for opposing_signal in opposing_signals:
            for signal in self.signals:
                if signal.SignalID == opposing_signal:
                    if signal.SignalStatus == 1:
                        print(f"敌对信号{signal.SignalID}开放，无法选排")
                        return
        # 判断区段是否被锁闭
        for track_id in track_ids:
            for track in self.tracks:
                if track.TrackID == track_id:
                    if track.LockFlag == 1:
                        print(f"区段{track.TrackID}已被锁闭，无法选排")
                        return
        # 判断照查条件
        # 判断道岔是否锁闭
        for switch_id in switch_ids.keys():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.LockFlag == 1:
                        print(f"道岔{switch.SwitchID}被锁闭，无法选排")
                        return
        # 判断道岔是否被封锁
        for switch_id in switch_ids.keys():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.FuncLockFlag == 1:
                        print(f"道岔{switch.SwitchID}被封锁，无法选排")
                        return

        # 征用道岔、区段、信号机
        for track_id in track_ids:
            for track in self.tracks:
                if track.TrackID == track_id:
                    track.UsedFlag = 1
                    print(f"区段{track.TrackID}被征用")
        for signal in self.signals:
            if signal.SignalID == signal_id:
                signal.UsedFlag = 1
                print(f"信号机{signal.SignalID}被征用")
        for switch_id in switch_ids.keys():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    switch.UsedFlag = 1
                    print(f"道岔{switch.SwitchID}被征用")

        # 转动道岔
        for switch_id, status in switch_ids.items():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.SwitchStatus != status:
                        print(f"道岔{switch.SwitchID}未处于规定位置")
                        if switch.FuncLockFlag == 1:
                            print(f"道岔{switch.SwitchID}被单锁，无法选排")
                            return
                        else:
                            # 将该道岔转动至规定位置
                            switch.SwitchStatus = status

        print("进路选排成功")

    def route_lock(self, route_id):
        """
        进路锁闭函数
        """
        print("执行进路锁闭")
        signal_id = self.interlockTable[route_id - 1].signal_name
        track_ids = self.interlockTable[route_id - 1].track_sections
        switch_ids = self.interlockTable[route_id - 1].switches
        opposing_signals = self.interlockTable[route_id - 1].opposing_signals

        # 判断敌对信号是否开放
        for opposing_signal in opposing_signals:
            for signal in self.signals:
                if signal.SignalID == opposing_signal:
                    if signal.SignalStatus == 1:
                        print(f"敌对信号{signal.SignalID}开放，进路无法锁闭")
                        return
        # 判断区段是否空闲以及是否被锁闭
        for tarck_id in track_ids:
            for track in self.tracks:
                if track.TrackID == tarck_id:
                    if track.TrackStatus == 1:
                        print(f"区段{track.TrackID}已被占用，进路无法锁闭")
                        return
                    if track.LockFlag == 1:
                        print(f"区段{track.TrackID}已被锁闭，进路无法锁闭")
                        return
        # 判断照查条件
        # 判断道岔是否在规定位置、是否锁闭、是否被封锁
        for switch_id, status in switch_ids.items():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.SwitchStatus != status:
                        print(f"道岔{switch.SwitchID}未处于规定位置,进路无法锁闭")
                        return
                    if switch.LockFlag == 1:
                        print(f"道岔{switch.SwitchID}已经锁闭,进路无法锁闭")
                        return
                    if switch.FuncLockFlag == 1:
                        print(f"道岔{switch.SwitchID}被封锁，进路无法锁闭")
                        return
        # 锁闭进路中的道岔、区段
        for switch_id in switch_ids.keys():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    switch.LockFlag = 1
                    print(f"道岔{switch.SwitchID}锁闭")
        for track_id in track_ids:
            for track in self.tracks:
                if track.TrackID == track_id:
                    track.LockFlag = 1
                    print(f"区段{track.TrackID}锁闭")
        # 清除征用标志
        for switch_id in switch_ids.keys():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    switch.UsedFlag = 0
                    print(f"道岔{switch.SwitchID}清除征用标志")
        for track_id in track_ids:
            for track in self.tracks:
                if track.TrackID == track_id:
                    track.UsedFlag = 0
                    print(f"区段{track.TrackID}清除征用标志")
        for signal in self.signals:
            if signal.SignalID == signal_id:
                signal.UsedFlag = 0
                print(f"信号机{signal.SignalID}清除征用标志")

        print("进路锁闭成功")

    def signal_open(self, route_id):
        """
        信号开放函数
        """
        print("执行信号开放")
        signal_id = self.interlockTable[route_id - 1].signal_name
        track_ids = self.interlockTable[route_id - 1].track_sections
        switch_ids = self.interlockTable[route_id - 1].switches
        opposing_signals = self.interlockTable[route_id - 1].opposing_signals

        # 判断敌对信号是否开放
        for opposing_signal in opposing_signals:
            for signal in self.signals:
                if signal.SignalID == opposing_signal:
                    if signal.SignalStatus == 1:
                        print(f"敌对信号{signal.SignalID}开放，信号无法正常开放")
                        return
        # 判断进站信号机红灯灯丝完好
        for signal in self.signals:
            if signal.SignalID == signal_id:
                if signal.FilamentStatus == 1:
                    print(f"信号机{signal.SignalID}红灯灯丝损坏，信号无法正常开放")
                    return
        # 判断区段是否空闲以及是否被锁闭
        for tarck_id in track_ids:
            for track in self.tracks:
                if track.TrackID == tarck_id:
                    if track.TrackStatus == 1:
                        print(f"区段{track.TrackID}已被占用，信号无法正常开放")
                        return
                    if track.LockFlag == 0:
                        print(f"区段{track.TrackID}还未锁闭，信号无法正常开放")
                        return
        # 判断照查条件
        # 判断道岔是否在规定位置、是否锁闭
        for switch_id, status in switch_ids.items():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.SwitchStatus != status:
                        print(f"道岔{switch.SwitchID}未处于规定位置,信号无法正常开放")
                        return
                    if switch.LockFlag == 0:
                        print(f"道岔{switch.SwitchID}还未锁闭,信号无法正常开放")
                        return
        # 开放信号机
        for signal in self.signals:
            if signal.SignalID == signal_id:
                signal.SignalStatus = 1

        print("信号开放成功")

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
