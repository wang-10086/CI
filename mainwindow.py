import sys
from device_data import Signal, Switch, Track, Button
from route import Route
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QPushButton


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1500, 900)
        self.setStyleSheet("QWidget { background-color: black; }")
        self.retranslateUi(Form)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


class MainWindow(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        signal_data_path = 'signal_data.txt'
        track_data_path = 'track_data.txt'
        joint_data_path = 'joint_data.txt'
        button_data_path = 'button_data.txt'

        self.signals = []
        self.switches = []
        self.tracks = []
        self.joints = []
        self.buttons = []

        # 轨道区段
        with open(track_data_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split(':')
                    track_id = parts[0].strip()
                    coords = parts[1].strip().split(',')
                    start_x, start_y = int(coords[0]), int(coords[1])
                    end_x, end_y = int(coords[2]), int(coords[3])
                    track = Track(track_id)
                    track.start_point = [start_x, start_y]
                    track.end_point = [end_x, end_y]
                    self.tracks.append(track)
        # 绝缘节等
        with open(joint_data_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split(':')
                    joint_id = parts[0].strip()
                    coords = parts[1].strip().split(',')
                    start_x, start_y = int(coords[0]), int(coords[1])
                    end_x, end_y = int(coords[2]), int(coords[3])
                    joint = Track(joint_id)
                    joint.start_point = [start_x, start_y]
                    joint.end_point = [end_x, end_y]
                    self.joints.append(joint)

        # 信号机按钮
        with open(button_data_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split(':')
                    button_id = parts[0].strip()
                    coords = parts[1].strip().split(',')
                    location_x, location_y = int(coords[0]), int(coords[1])
                    button = Button(button_id)
                    button.point = [location_x, location_y]
                    self.buttons.append(button)
        # 信号机
        with open(signal_data_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split(':')
                    signal_id = parts[0].strip()
                    coords = parts[1].strip().split(',')
                    location_x, location_y = int(coords[0]), int(coords[1])
                    signal = Signal(signal_id)
                    signal.point = [location_x, location_y]
                    self.signals.append(signal)

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
        # for track in self.tracks:
        #     print(
        #         f"区段编号: {track.TrackID}, 状态: {track.TrackStatus}, 征用状态: {track.UsedFlag}, 起点坐标: {track.start_point}, 终点坐标: {track.end_point}")

        route = Route(
            route_id=1,
            route_type="进路类型1",
            route_prop="属性1",
            start_btn_id="BtnStart",
            end_btn_id="BtnEnd",
            signal_id="S001",
            conf_signal_num=2,
            conf_signal_id=["S002", "S003"],
            conf_condition="条件1",
            switch_num=3,
            switch_id=["SW1", "SW2", "SW3"],
            switch_pos=["Pos1", "Pos2", "Pos3"],
            protect_switch_num=1,
            protect_switch_id=["PS1"],
            protect_switch_pos=["PPos1"],
            track_num=4,
            track_id=["T001", "T002", "T003", "T004"]
        )
        self.interlockTable = [route]

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

        # 绘制绝缘节等
        for joint in self.joints:
            pen = QPen(linecolor, linewidth, Qt.SolidLine)  # 红色线条，宽度为3
            painter.setPen(pen)
            start_point = QPoint(joint.start_point[0], joint.start_point[1])
            end_point = QPoint(joint.end_point[0], joint.end_point[1])
            painter.drawLine(start_point, end_point)

        # 绘制按钮
        for button in self.buttons:
            self.createButton(button.ButtonID, button.point)

        for signal in self.signals:
            pen = QPen(linecolor, linewidth, Qt.SolidLine)
            painter.setPen(pen)
            painter.setBrush(QBrush(QColor(255, 0, 0)))  # 使用红色填充
            center_point = QPoint(signal.point[0], signal.point[1])
            radius = 10  # 圆形的半径
            painter.drawEllipse(center_point, radius, radius)

    def createButton(self, name, pos):
        """创建按钮"""
        btn = QPushButton(name, self)
        btn.move(*pos)
        btn.setStyleSheet("QPushButton { background-color: rgb(192, 192, 192); }")
        btn.setFixedSize(21, 21)
        btn.show()
        btn.clicked.connect(lambda checked, name=name: self.onButtonClick(name))

    def update_ui(self):
        """
        更新界面控件参数
        """
        pass

    def route_selection(self, route_id):
        """
        进路选排函数
        """
        print("执行进路选排")
        # 确认进路是否可用
        signal_id = self.interlockTable[route_id - 1].SignalID
        # 判断信号机是否可用
        for signal in self.signals:
            if signal.SignalID == signal_id:
                if signal.UsedFlag == 1:
                    print("信号机已征用")
                    return
                else:
                    # signal.UsedFlag = 1
                    break
        # 判断区段是否可用
        track_ids = self.interlockTable[route_id - 1].TrackID
        for tarck_id in track_ids:
            for track in self.tracks:
                if track.TrackID == tarck_id:
                    if track.UsedFlag == 0:
                        print("区段未被征用")
                    if track.TrackStatus == 0:
                        print("区段空闲")
                    if track.LockFlag == 0:
                        print("区段未锁闭")
        # 判断道岔是否可用
        switch_ids = self.interlockTable[route_id - 1].SwitchID
        for switch_id in switch_ids:
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.UsedFlag == 0:
                        print("道岔未被征用")
                    if switch.LockFlag == 0:
                        print("道岔未锁闭")

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
