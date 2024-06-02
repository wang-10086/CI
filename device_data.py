class Signal:
    def __init__(self, signal_ID):
        """
        初始化信号机类
        :param SignalID: 信号机编号
        :param SignalStatus: 点灯状态
        :param FilamentStatus: 信号机灯丝状态
        :param UsedFlag: 信号机征用状态
        :param LockFlag: 信号机锁闭标志
        :param OpenedFlag: 信号机曾开放标志
        :param SignalControl: 点灯命令控制标志
        """
        self.SignalID = signal_ID
        self.SignalStatus = 0
        self.FilamentStatus = 0
        self.UsedFlag = 0
        self.LockFlag = 0
        self.OpenedFlag = 0
        self.SignalControl = 0


class Switch:
    def __init__(self, switch_ID):
        """
        初始化道岔类
        :param SwitchID: 道岔编号
        :param SwitchStatus: 道岔状态
        :param UsedFlag: 道岔征用状态
        :param LockFlag: 道岔锁闭标志
        :param FuncLockFlag: 道岔功能锁闭标志
        :param CallonLockFlag: 道岔调车锁闭标志
        :param SwitchControl: 道岔控制标志
        :param DelayParameter: 道岔延时参数
        """
        self.SwitchID = switch_ID
        self.SwitchStatus = 0
        self.UsedFlag = 0
        self.LockFlag = 0
        self.FuncLockFlag = 0
        self.CallonLockFlag = 0
        self.SwitchControl = 0
        self.DelayParameter = 0


class Track:
    def __init__(self, track_ID):
        """
        初始化轨道类
        :param TrackID: 区段编号
        :param Track_Status: 区段状态
        :param UsedFlag: 区段征用状态
        :param LockFlag: 区段锁闭标志
        :param OccupiedFlag: 区段曾占用标志
        :param start_point: 区段起点
        :param end_point: 区段终点
        """
        self.TrackID = track_ID
        self.TrackStatus = 0
        self.UsedFlag = 0
        self.LockFlag = 0
        self.OccupiedFlag = 0
        self.start_point = None
        self.end_point = None

class Button:
    def __init__(self, button_ID):
        """
        初始化轨道类
        :param ButtonID: 区段编号
        :param Track_Status: 区段状态
        :param UsedFlag: 区段征用状态
        :param LockFlag: 区段锁闭标志
        :param OccupiedFlag: 区段曾占用标志
        :param start_point: 区段起点
        :param end_point: 区段终点
        """
        self.ButtonID = button_ID
        self.point = None
