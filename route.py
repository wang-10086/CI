class Route:
    def __init__(self, route_id, route_type, route_prop, start_btn_id, end_btn_id, signal_id, conf_signal_num, conf_signal_id,
                 conf_condition, switch_num, switch_id, switch_pos, protect_switch_num, protect_switch_id, protect_switch_pos,
                 track_num, track_id):
        self.RouteID = route_id
        self.RouteType = route_type
        self.RouteProp = route_prop
        self.StartBtnID = start_btn_id
        self.EndBtnID = end_btn_id
        self.SignalID = signal_id
        self.ConfSignalNum = conf_signal_num
        self.ConfSignalID = conf_signal_id
        self.ConfCondition = conf_condition
        self.SwitchNum = switch_num
        self.SwitchID = switch_id
        self.SwitchPos = switch_pos
        self.ProtectSwitchNum = protect_switch_num
        self.ProtectSwitchID = protect_switch_id
        self.ProtectSwitchPos = protect_switch_pos
        self.TrackNum = track_num
        self.TrackID = track_id

    def __str__(self):
        return (f"Route(RouteID={self.RouteID}, RouteType={self.RouteType}, RouteProp={self.RouteProp}, "
                f"StartBtnID={self.StartBtnID}, EndBtnID={self.EndBtnID}, SignalID={self.SignalID}, "
                f"ConfSignalNum={self.ConfSignalNum}, ConfSignalID={self.ConfSignalID}, ConfCondition={self.ConfCondition}, "
                f"SwitchNum={self.SwitchNum}, SwitchID={self.SwitchID}, SwitchPos={self.SwitchPos}, "
                f"ProtectSwitchNum={self.ProtectSwitchNum}, ProtectSwitchID={self.ProtectSwitchID}, "
                f"ProtectSwitchPos={self.ProtectSwitchPos}, TrackNum={self.TrackNum}, TrackID={self.TrackID})")


# 示例使用
if __name__ == '__main__':
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

    print(route)
