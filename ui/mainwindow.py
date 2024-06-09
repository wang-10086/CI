import sys
from ui.ui_data import SignalButton, SwitchButton
from ui.ui_form import Ui_Form
from utils.read_files import readInterlockTable, read_tracks, read_signals, read_joints, read_switches
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit


class MainWindow(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        interlock_table_path = './data/联锁表.xlsx'
        signal_data_path = './data/signal_data.txt'
        track_data_path = './data/track_data.txt'
        joint_data_path = './data/joint_data.txt'
        switch_data_path = './data/switch_data.txt'

        # 记录点击的信号机ID
        self.first_signal_id = None
        self.second_signal_id = None
        self.cancelFlag = 0  # 记录是否取消进路
        self.current_routes = []  # 添加这个属性用于保存当前选排的进路信息
        self.cancel_route = None  # 记录要取消的进路

        # 读取设备数据
        self.tracks = read_tracks(track_data_path)  # 轨道区段
        self.joints = read_joints(joint_data_path)  # 绝缘节
        self.signals = read_signals(signal_data_path)  # 信号机
        self.switches = read_switches(switch_data_path)  # 道岔

        # 读取联锁表
        self.interlockTable = readInterlockTable(interlock_table_path)

        # 绘制信号机按钮
        self.signal_btns = []
        for signal in self.signals:
            signal_button = SignalButton(signal.SignalID, self)
            if signal.direction == 1:
                signal_button.point = [signal.point[0] + 13, signal.point[1] - 7]
            else:
                signal_button.point = [signal.point[0] - 28, signal.point[1] - 7]
            signal_button.move(*signal_button.point)
            signal_button.setStyleSheet("QPushButton { background-color: rgb(192, 192, 192); }")
            signal_button.setFixedSize(14, 14)
            signal_button.clicked.connect(lambda checked, name=signal.SignalID: self.onButtonClick(name))
            self.signal_btns.append(signal_button)

        # 绘制道岔按钮
        self.switch_btns = []
        for switch in self.switches:
            # 计算线条中点
            x = switch.start_point[0]
            y = switch.end_point_0[1] + 5
            # 绘制道岔按钮
            switch_btn = SwitchButton(switch.SwitchID, switch.SwitchID, self)
            font1 = QFont()
            font1.setPointSize(8)
            switch_btn.setFont(font1)
            switch_btn.point = [x, y]
            switch_btn.move(*switch_btn.point)
            switch_btn.setStyleSheet("QPushButton { color: white; background-color: rgba(255, 255, 255, 0); }")
            switch_btn.setFixedSize(15, 15)
            self.switch_btns.append(switch_btn)

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
        linewidth = 2

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

            # # 计算线条中点
            # mid_x = (track.start_point[0] + track.end_point[0]) // 2
            # mid_y = track.end_point[1] - 5
            #
            # font = QFont()
            # font.setPointSize(8)  # 改变字体的大小
            # painter.setFont(font)
            # # 绘制线条名称
            # painter.setPen(QColor(255, 255, 255))  # 设置文字颜色为白色
            # painter.drawText(mid_x, mid_y, track.TrackID)  # 在中点绘制线条名称

        # 绘制绝缘节等
        for joint in self.joints:
            pen = QPen(linecolor, linewidth, Qt.SolidLine)  # 白色线条，宽度为3
            painter.setPen(pen)
            start_point = QPoint(joint.start_point[0], joint.start_point[1])
            end_point = QPoint(joint.end_point[0], joint.end_point[1])
            painter.drawLine(start_point, end_point)

        # 绘制信号机
        for signal in self.signals:
            radius = 6  # 圆形的半径
            font = QFont()
            font.setPointSize(8)  # 改变字体的大小
            pen = QPen(linecolor, linewidth, Qt.SolidLine)
            painter.setPen(pen)
            if signal.SignalID[0] == 'D':
                # 调车信号机
                if signal.SignalStatus == 1:
                    painter.setBrush(QBrush(QColor(0, 0, 255)))  # 蓝色表示信号机开放
                else:
                    painter.setBrush(QBrush(QColor(224, 224, 224)))  # 灰色表示信号机关闭
                center_point = QPoint(signal.point[0], signal.point[1])
                painter.drawEllipse(center_point, radius, radius)
                # 绘制信号机名称
                painter.setFont(font)
                painter.setPen(QColor(255, 255, 255))  # 设置文字颜色为白色
                if signal.direction == 0:
                    painter.drawText(signal.point[0], signal.point[1] - 2 * radius, signal.SignalID)    # 下行方向
                else:
                    painter.drawText(signal.point[0], signal.point[1] + 4 * radius, signal.SignalID)    # 上行方向
            else:
                # 列车信号机
                # 绘制第一个信号机
                if signal.SignalStatus == 1:
                    painter.setBrush(QBrush(QColor(0, 255, 0)))  # 绿色表示信号机开放
                else:
                    painter.setBrush(QBrush(QColor(255, 0, 0)))  # 红色表示信号机关闭
                center_point = QPoint(signal.point[0], signal.point[1])
                painter.drawEllipse(center_point, radius, radius)
                # 绘制第二个信号机
                painter.setPen(pen)
                painter.setBrush(QBrush(QColor(0, 0, 0)))  # 列车信号机使用黑色填充
                if signal.direction == 1:
                    center_point = QPoint(signal.point[0] - 2 * radius, signal.point[1])
                    text_point = signal.point[1] + 4 * radius
                else:
                    center_point = QPoint(signal.point[0] + 2 * radius, signal.point[1])
                    text_point = signal.point[1] - 2 * radius
                painter.drawEllipse(center_point, radius, radius)
                # 绘制信号机名称
                painter.setFont(font)
                painter.setPen(QColor(255, 255, 255))  # 设置文字颜色为白色
                painter.drawText(signal.point[0], text_point, signal.SignalID)  # 在中点绘制线条名称

        # 绘制道岔
        for switch in self.switches:
            start_point = QPoint(switch.start_point[0], switch.start_point[1])
            if switch.SwitchStatus == 0:
                end_point = QPoint(switch.end_point_0[0], switch.end_point_0[1])
            else:
                end_point = QPoint(switch.end_point_1[0], switch.end_point_1[1])

            if switch.LockFlag == 0:
                pen = QPen(QColor(0, 0, 255), linewidth, Qt.SolidLine)  # 未锁闭显示蓝色
            else:
                pen = QPen(QColor(224, 224, 224), linewidth, Qt.SolidLine)  # 未锁闭显示灰白色
            painter.setPen(pen)
            painter.drawLine(start_point, end_point)

    def onButtonClick(self, name):
        """点击信号机按钮
        1.排列进路
        2.取消进路
        """
        if self.cancelFlag == 0:
            if self.first_signal_id is None:
                self.first_signal_id = name
                self.addMessage(f"选中了始端信号机: {name}")
            else:
                self.second_signal_id = name
                self.addMessage(f"选中了终端信号机: {name}")
                self.search_route()  # 排列进路

        elif self.cancelFlag == 1:
            for rt in self.current_routes:
                if name == rt.start_button:  # 如果点击的信号机是之前选排的始端信号机
                    self.cancel_route = rt
                    break

            if self.cancel_route is None:
                self.addMessage(f"没有找到匹配的进路")
            else:
                self.addMessage(f"取消进路: {self.cancel_route.start_button} -> {self.cancel_route.end_button}")
                self.route_cancel()  # 取消进路
                self.current_routes.remove(self.cancel_route)  # 从当前选排的进路中移除
                self.cancelFlag = 0

    def search_route(self):
        """
        1. 遍历联锁表，找到符合条件的进路
        2. 执行进路选排
        3. 执行进路锁闭
        4. 执行信号开放
        5. 更新界面
        """
        isFind = False
        for route in self.interlockTable:
            if route.start_button == self.first_signal_id and route.end_button == self.second_signal_id:
                isFind = True
                self.addMessage(f"办理进路: {route.start_button} -> {route.end_button}")
                self.current_routes.append(route)  # 保存当前进路信息

                try:
                    self.addMessage(f"办理进路{route.route_number}")
                    self.route_selection(route.route_number)
                    self.route_lock(route.route_number)
                    self.signal_open(route.route_number)
                    self.update()
                    print("办理进路成功")
                except Exception as e:
                    print(e)
        if not isFind:
            self.addMessage("未找到符合条件的进路")

        # 重置信号机ID
        self.first_signal_id = None
        self.second_signal_id = None

    def on_zongrenjie_click(self):
        """总人解按钮点击事件"""
        password, ok = QInputDialog.getText(self, "密码输入", "请输入密码:", QLineEdit.Password)

        if ok and password == "1234":  # 将 "正确密码" 替换为你实际使用的密码
            self.textEdit.append("密码正确，进行下一步操作")
            QMessageBox.information(self, "信息", "密码正确，进行下一步操作")
            self.cancelFlag = 1

            self.addMessage("总人解")

        else:
            self.textEdit.append("密码错误")
            QMessageBox.warning(self, "警告", "密码错误")

    def on_zongquxiao_click(self):
        """总取消按钮点击事件"""
        # password, ok = QInputDialog.getText(self, "密码输入", "请输入密码:", QLineEdit.Password)

        # if ok and password == "1234":  # 将 "正确密码" 替换为你实际使用的密码
        #    self.textEdit.append("密码正确，进行下一步操作")
        #    QMessageBox.information(self, "信息", "密码正确，进行下一步操作")

        # self.cancelFlag = 1
        # self.addMessage("总取消")

        # else:
        #    self.textEdit.append("密码错误")
        #    QMessageBox.warning(self, "警告", "密码错误")
        self.cancelFlag = 1
        self.addMessage("总取消")

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
            try:
                self.addMessage(f"办理进路{route_id}")
                self.route_selection(route_id)
                self.route_lock(route_id)
                self.signal_open(route_id)
                self.update()
                print("办理进路成功")
            except Exception as e:
                print(e)

    def route_selection(self, route_id):
        """
        进路选排函数
        """
        print("执行进路选排")
        signal_ids = self.interlockTable[route_id - 1].signal_name
        track_ids = self.interlockTable[route_id - 1].track_sections
        switch_ids = self.interlockTable[route_id - 1].switches
        opposing_signals = self.interlockTable[route_id - 1].opposing_signals

        # 判断信号机是否被征用
        for signal_id in signal_ids:
            for signal in self.signals:
                if signal.SignalID == signal_id:
                    if signal.UsedFlag == 1:
                        raise Exception(f"信号机{signal.SignalID}已被征用，无法选排")
        # 判断区段是否空闲
        for tarck_id in track_ids:
            for track in self.tracks:
                if track.TrackID == tarck_id:
                    if track.TrackStatus == 1:
                        raise Exception(f"区段{track.TrackID}已被占用，无法选排")
        # 判断区段是否被征用
        for track_id in track_ids:
            for track in self.tracks:
                if track.TrackID == track_id:
                    if track.UsedFlag == 1:
                        raise Exception(f"区段{track.TrackID}被征用，无法选排")
        # 判断道岔是否被征用
        for switch_id in switch_ids.keys():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.UsedFlag == 1:
                        raise Exception(f"道岔{switch.SwitchID}被征用，无法选排")
        # 判断敌对信号是否开放
        for opposing_signal in opposing_signals:
            for signal in self.signals:
                if signal.SignalID == opposing_signal:
                    if signal.SignalStatus == 1:
                        raise Exception(f"敌对信号{signal.SignalID}开放，无法选排")
        # 判断区段是否被锁闭
        for track_id in track_ids:
            for track in self.tracks:
                if track.TrackID == track_id:
                    if track.LockFlag == 1:
                        raise Exception(f"区段{track.TrackID}已被锁闭，无法选排")
        # 判断照查条件
        # 判断道岔是否锁闭
        for switch_id in switch_ids.keys():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.LockFlag == 1:
                        raise Exception(f"道岔{switch.SwitchID}已被锁闭，无法选排")
        # 判断道岔是否被封锁
        for switch_id in switch_ids.keys():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.FuncLockFlag == 1:
                        raise Exception(f"道岔{switch.SwitchID}被封锁，无法选排")

        # 征用道岔、区段、信号机
        for track_id in track_ids:
            for track in self.tracks:
                if track.TrackID == track_id:
                    track.UsedFlag = 1
                    print(f"区段{track.TrackID}被征用")
        for signal_id in signal_ids:
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
                        else:
                            # 将该道岔转动至规定位置
                            switch.SwitchStatus = status

        print("进路选排成功")

    def route_lock(self, route_id):
        """
        进路锁闭函数
        """
        print("执行进路锁闭")
        signal_ids = self.interlockTable[route_id - 1].signal_name
        track_ids = self.interlockTable[route_id - 1].track_sections
        switch_ids = self.interlockTable[route_id - 1].switches
        opposing_signals = self.interlockTable[route_id - 1].opposing_signals

        # 判断敌对信号是否开放
        for opposing_signal in opposing_signals:
            for signal in self.signals:
                if signal.SignalID == opposing_signal:
                    if signal.SignalStatus == 1:
                        raise Exception(f"敌对信号{signal.SignalID}开放，进路无法锁闭")
        # 判断区段是否空闲以及是否被锁闭
        for tarck_id in track_ids:
            for track in self.tracks:
                if track.TrackID == tarck_id:
                    if track.TrackStatus == 1:
                        raise Exception(f"区段{track.TrackID}已被占用，进路无法锁闭")
                    if track.LockFlag == 1:
                        raise Exception(f"区段{track.TrackID}已被锁闭，进路无法锁闭")
        # 判断照查条件
        # 判断道岔是否在规定位置、是否锁闭、是否被封锁
        for switch_id, status in switch_ids.items():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.SwitchStatus != status:
                        raise Exception(f"道岔{switch.SwitchID}未处于规定位置,进路无法锁闭")
                    if switch.LockFlag == 1:
                        raise Exception(f"道岔{switch.SwitchID}已经锁闭,进路无法锁闭")
                    if switch.FuncLockFlag == 1:
                        raise Exception(f"道岔{switch.SwitchID}被封锁，进路无法锁闭")
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
        for signal_id in signal_ids:
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
        signal_ids = self.interlockTable[route_id - 1].signal_name
        track_ids = self.interlockTable[route_id - 1].track_sections
        switch_ids = self.interlockTable[route_id - 1].switches
        opposing_signals = self.interlockTable[route_id - 1].opposing_signals

        # 判断敌对信号是否开放
        for opposing_signal in opposing_signals:
            for signal in self.signals:
                if signal.SignalID == opposing_signal:
                    if signal.SignalStatus == 1:
                        raise Exception(f"敌对信号{signal.SignalID}开放，信号无法正常开放")
        # 判断进站信号机红灯灯丝完好
        for signal_id in signal_ids:
            for signal in self.signals:
                if signal.SignalID == signal_id:
                    if signal.FilamentStatus == 1:
                        raise Exception(f"信号机{signal.SignalID}红灯灯丝损坏，信号无法正常开放")
        # 判断区段是否空闲以及是否被锁闭
        for tarck_id in track_ids:
            for track in self.tracks:
                if track.TrackID == tarck_id:
                    if track.TrackStatus == 1:
                        raise Exception(f"区段{track.TrackID}已被占用，信号无法正常开放")
                    if track.LockFlag == 0:
                        raise Exception(f"区段{track.TrackID}还未锁闭，信号无法正常开放")
        # 判断照查条件
        # 判断道岔是否在规定位置、是否锁闭
        for switch_id, status in switch_ids.items():
            for switch in self.switches:
                if switch.SwitchID == switch_id:
                    if switch.SwitchStatus != status:
                        raise Exception(f"道岔{switch.SwitchID}未处于规定位置,信号无法正常开放")
                    if switch.LockFlag == 0:
                        raise Exception(f"道岔{switch.SwitchID}还未锁闭,信号无法正常开放")
        # 开放信号机
        for signal_id in signal_ids:
            for signal in self.signals:
                if signal.SignalID == signal_id:
                    signal.SignalStatus = 1

        print("信号开放成功")

    def signal_hold_open(self):
        """
        信号开放保持函数
        """
        pass

    def route_normal_unlock(self):
        """
        进路正常解锁函数
        """
        pass

    def route_cancel(self):
        """
        进路取消函数
        """
        if self.cancel_route:
            signal_ids = self.cancel_route.signal_name
            track_ids = self.cancel_route.track_sections
            switch_ids = self.cancel_route.switches

            # 关闭信号机
            for signal_id in signal_ids:
                for signal in self.signals:
                    if signal.SignalID == signal_id:
                        signal.SignalStatus = 0

            # 解锁道岔
            for switch_id in switch_ids.keys():
                for switch in self.switches:
                    if switch.SwitchID == switch_id:
                        switch.LockFlag = 0
                        print(f"道岔{switch.SwitchID}解锁")

            # 解锁区段
            for track_id in track_ids:
                for track in self.tracks:
                    if track.TrackID == track_id:
                        track.LockFlag = 0
                        print(f"区段{track.TrackID}解锁")

            self.addMessage(f"进路取消: {self.cancel_route.start_button} -> {self.cancel_route.end_button}")
            self.update()

        else:
            self.addMessage("没有选排的进路需要取消")

    def driving_simulation(self):
        """
        模拟行车函数
        """
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
