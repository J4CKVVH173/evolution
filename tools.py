class Accident(Exception):

    def __init__(self, msg):
        self.msg = msg

    def msg_print(self):
        return self.msg


def set_position(cells: list) -> dict:
    positions = dict()
    for cell in cells:
        positions[cell.get_id()] = 'cell'

    return positions
