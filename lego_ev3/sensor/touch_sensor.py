import PyRSquared.lego_ev3.sensor.sensor as sensor


class TouchSensor(sensor.Sensor):
    def __init__(self, ev3_parent, port):
        super().__init__(ev3_parent, port)
        self.type_number = 16

    def is_pressed(self) -> bool:
        return bool(self.read_mode(0))

    def count_presses(self) -> int:
        return int(self.read_mode(1))
