class Transition:

    def __init__(self, write_symbol, movement, next_state):
        self.write_symbol = write_symbol
        self.movement = movement
        self.next_state = next_state

    def __str__(self):
        return f"Write: {self.write_symbol}, Move: {self.movement}, Next: {self.next_state}"
