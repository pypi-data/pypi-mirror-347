# Represents a single transition in the Turing Machine
class Transition:

    def __init__(self, write_symbol, movement, next_state):
        self.write_symbol = write_symbol
        self.movement = movement  # ? Direction to move the head ("L" or "R")
        self.next_state = next_state

    def __str__(self):
        return f"Write: {self.write_symbol}, Move: {self.movement}, Next: {self.next_state}"


# Simulates a simple Turing Machine for unary addition
class TuringMachine:

    def __init__(self, input_tape):
        self.blank_symbol = "B"
        self.current_state = "q0"
        self.accept_state = "q3"

        # ? Tape represented as a list of symbols "11+1" -> ["1", "1", "1", "+", "1"]
        self.tape = list(input_tape)
        self.head_position = 0  # Current position of the head
        # Build the state transition rules
        self.transitions = self._build_addition_rules()

    # Execute the Turing Machine until it reaches the accept state
    def execute(self):
        while self.current_state != self.accept_state:
            current_symbol = self._read_current_symbol()

            # If no transition is defined for the current state and symbol, return with failure
            if (
                self.current_state not in self.transitions
                or current_symbol not in self.transitions[self.current_state]
            ):
                return ""

            # Get the appropriate transition
            transition = self.transitions[self.current_state][current_symbol]

            # Perform the actions: write, move, and change state
            self._write_symbol(transition.write_symbol)
            self._move_head(transition.movement)
            self.current_state = transition.next_state

        # Return the resulting tape content without blank symbols
        return "".join(self.tape).strip(self.blank_symbol)

    # Define the transition rules for unary addition (e.g., "111+11" -> "11111")
    def _build_addition_rules(self):
        transitions = {}

        # In state q0: move right over all 1s, when '+' is found, replace with 1 and move to q1
        transitions["q0"] = {
            "1": Transition("1", "R", "q0"),  # Keep moving over 1s
            "+": Transition("1", "R", "q1"),  # Replace '+' with '1' and move to q1
        }

        # In state q1: move right over all 1s until the blank symbol'B' is found
        transitions["q1"] = {
            "1": Transition("1", "R", "q1"),  # Keep moving over 1s
            # Go left when blank is found
            self.blank_symbol: Transition(self.blank_symbol, "L", "q2"),
        }

        # In state q2: remove the last 1 (rightmost one from the second number) and go to accept state
        transitions["q2"] = {
            # Remove a '1' and halt
            "1": Transition(self.blank_symbol, "L", self.accept_state)
        }

        return transitions

    # Add a blank cell if the head moves off the left or right end of the tape
    def _extend_tape_if_needed(self):
        if self.head_position < 0:
            self.tape.insert(0, self.blank_symbol)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)

    # Read the symbol at the current tape head position
    def _read_current_symbol(self):
        self._extend_tape_if_needed()
        return self.tape[self.head_position]

    # Write a symbol at the current tape head position
    def _write_symbol(self, symbol):
        self._extend_tape_if_needed()
        self.tape[self.head_position] = symbol

    # Move the tape head left or right
    def _move_head(self, direction):
        if direction == "L":
            self.head_position -= 1
        elif direction == "R":
            self.head_position += 1
