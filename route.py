class Route:
    def __init__(self, route_number, start_button, end_button, signal_name, signal_display, switches, opposing_signals, track_sections):
        self.route_number = route_number
        self.start_button = start_button
        self.end_button = end_button
        self.signal_name = signal_name
        self.signal_display = signal_display
        self.switches = switches  # Dictionary of switches and their states
        self.opposing_signals = opposing_signals
        self.track_sections = track_sections

    def __repr__(self):
        return f"Route({self.route_number}, {self.start_button}, {self.end_button}, {self.signal_name}, {self.signal_display}, {self.switches}, {self.opposing_signals}, {self.track_sections})"

    def display_route_info(self):
        """Display detailed information about the route."""
        print(f"Route Number: {self.route_number}", end=" ")
        print(f"Start Button: {self.start_button}", end=" ")
        print(f"End Button: {self.end_button}", end=" ")
        print(f"Signal Name: {self.signal_name}", end=" ")
        print(f"Signal Display: {self.signal_display}", end=" ")
        print(f"Switches: {self.switches}", end=" ")
        print(f"Opposing Signals: {self.opposing_signals}", end=" ")
        print(f"Track Sections: {self.track_sections}")


if __name__ == '__main__':
    # Example usage
    switches = {
        "Switch1": 0,
        "Switch2": 0,
        "Switch3": 1
    }

    route = Route(
        route_number=1,
        start_button="ButtonA",
        end_button="ButtonB",
        signal_name="SignalX",
        signal_display="Green",
        switches=switches,
        opposing_signals=["SignalY", "SignalZ"],
        track_sections=["Section1", "Section2", "Section3"]
    )

    route.display_route_info()
