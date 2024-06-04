import pandas as pd
import re

from route import Route
from device_data import Track, Switch, Button, Signal


# Helper function to parse switches
def parse_switches(switch_str):
    switches = {}
    if pd.isna(switch_str):
        return switches
    for item in re.split(r'[,\s]+', switch_str):
        if "(" in item or "[" in item:
            item = item.strip("()[]")
            switches[item] = 1  # 道岔处于反位
        else:
            switches[item] = 0  # 道岔处于定位
    return switches


def readInterlockTable(excel_path):
    # Extract route information from the dataframe

    # Load the Excel file
    df = pd.read_excel(excel_path)
    routes = []
    for _, row in df.iterrows():
        route_number = row.get("进路序号")
        start_button = row.get("排列进路按下起点按钮")
        end_button = row.get("排列进路按下终点按钮")
        signal_name = row.get("信号机名称")
        signal_display = row.get("信号机显示")
        switches = parse_switches(row.get("道岔"))
        opposing_signals = row.get("敌对信号").split(",") if not pd.isna(row.get("敌对信号")) else []
        track_sections = row.get("轨道区段").split(",") if not pd.isna(row.get("轨道区段")) else []

        route = Route(route_number=route_number, start_button=start_button, end_button=end_button,
                      signal_name=signal_name, signal_display=signal_display, switches=switches,
                      opposing_signals=opposing_signals, track_sections=track_sections)

        routes.append(route)

    return routes


def read_tracks(track_data_path):
    tracks = []
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
                tracks.append(track)

    return tracks


def read_signals(signal_data_path):
    signals = []
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
                signals.append(signal)

    return signals


def read_joints(joint_data_path):
    joints = []
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
                joints.append(joint)

    return joints


def read_buttons(button_data_path):
    buttons = []
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
                buttons.append(button)

    return buttons


def read_switches(switch_data_path):
    switchs = []
    with open(switch_data_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(':')
                switch_id = parts[0].strip()
                coords = parts[1].strip().split(',')
                start_x, start_y = int(coords[0]), int(coords[1])
                end_x, end_y = int(coords[2]), int(coords[3])
                switch = Switch(switch_id)
                switch.start_point = [start_x, start_y]
                switch.end_point = [end_x, end_y]
                switchs.append(switch)

    return switchs
