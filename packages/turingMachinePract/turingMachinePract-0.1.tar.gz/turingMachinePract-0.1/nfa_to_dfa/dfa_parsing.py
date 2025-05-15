from nfa_parsing import NFA


class DFA:
    def __init__(self, nfa: NFA):
        self.nfa_automaton = nfa

        # Compute ε-closure of the NFA's start state
        initial_closure = self._epsilon_closure(self.nfa_automaton.start_state)
        # ? DFA start state as a frozen set, to work as a key later, and if it's more than state, it will be considered as an one state
        self.start_state = frozenset(initial_closure)
        self.unvisited_states = [self.start_state]
        self.states = [self.start_state]

        self.alphabet = self.nfa_automaton.alphabet
        # ? Dict<frozenset(from), <symbol, frozenset(to)>
        self.transitions = {}
        self.accept_states = []

    # Main function to construct the DFA from the given NFA
    def dfa_equivalence(self):
        while len(self.unvisited_states) > 0:
            current = self.unvisited_states.pop()  # Get the next unprocessed state

            for symbol in self.alphabet:
                # Move using current symbol and then compute ε-closure of result
                move_result = self._move(current, symbol)
                closure = self._epsilon_closure(move_result)

                closure_frozen = frozenset(closure)

                # Add new DFA state if it's not already known
                if closure_frozen not in self.states:
                    self.states.append(closure_frozen)
                    self.unvisited_states.append(closure_frozen)

                # Initialize transition map if necessary
                if current not in self.transitions:
                    self.transitions[frozenset(current)] = {}

                # Register transition: δ(current, symbol) -> closure
                self.transitions[frozenset(current)][symbol] = closure_frozen

            # Mark state as accepting if it includes any NFA accepting state
            for state in closure:
                if state and state in self.nfa_automaton.accept_states:
                    if frozenset(closure) not in self.accept_states:
                        self.accept_states.append(frozenset(closure))

        # ? handle trap state
        trap_state = frozenset("⌀")

        for state in self.states:
            if state not in self.transitions:
                self.transitions[state] = {}

            for symbol in self.alphabet:
                if (
                    symbol not in self.transitions[state]
                    or not self.transitions[state][symbol]
                ):
                    self.transitions[state][symbol] = trap_state

        self.transitions[trap_state] = {}
        for symbol in self.alphabet:
            self.transitions[trap_state][symbol] = trap_state

        # Add trap state to DFA state list if it was actually used
        used = False
        for targets in self.transitions.values():
            # targets is a dict: symbol → target_state
            for target_state in targets.values():
                if target_state == trap_state:
                    used = True
                    break
            if used:
                break

        if used:
            self.states.append(trap_state)

    # Computes ε-closure of a set of states (i.e., all states reachable by ε-transitions)
    def _epsilon_closure(self, state):
        stack = list(state)
        closure = set(state)

        while len(stack) > 0:
            current = stack.pop()

            if "e" in self.nfa_automaton.transitions.get(current, {}):
                for next_state in self.nfa_automaton.transitions[current]["e"]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)

        return closure

    # Computes the set of states reachable from a set of states via a given symbol
    def _move(self, states, symbol):
        result = set()
        for state in states:
            if (
                state in self.nfa_automaton.transitions
                and symbol in self.nfa_automaton.transitions[state]
            ):
                result.update(self.nfa_automaton.transitions[state][symbol])
        return result

    # Pretty string representation of the DFA (states, transitions, etc.)
    def __str__(self):
        def format_state(state):
            return "{" + ", ".join(sorted(state)) + "}"

        result = []

        # States
        result.append("States: " + ", ".join(format_state(s) for s in self.states if s))
        result.append("Alphabet: " + ", ".join(sorted(self.alphabet)))
        result.append("Start State: " + format_state(self.start_state))
        result.append(
            "Accept States: " + ", ".join(format_state(s) for s in self.accept_states)
        )

        # Transitions
        result.append("Transitions:")
        for from_state, trans_dict in self.transitions.items():
            if not from_state:
                continue
            for symbol, to_state in trans_dict.items():
                result.append(
                    f"  δ({format_state(from_state)}, {symbol}) -> {{{', '.join(sorted(to_state))}}}"
                )

        return "\n".join(result)
