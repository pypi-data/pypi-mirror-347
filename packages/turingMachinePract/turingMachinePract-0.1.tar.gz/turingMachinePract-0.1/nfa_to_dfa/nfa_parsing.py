class NFA:
    def __init__(self, language):
        self.states = []
        self.alphabet = []
        self.start_state = None
        self.accept_states = []
        # ? Dict<from, <symbol, set(to)>
        self.transitions = {}
        # Process input string and build NFA
        self._process_language(language)

    def _process_language(self, language):
        """
        Parse an encoded NFA string into its components.
        Format:
        "q0;q1;q2#a;b#q0,a,q1;q1,e,q2;q2,b,q0#q0#q2;q1"
            Sections:
            0 - states
            1 - alphabet
            2 - transitions
            3 - start state
            4 - accept states
        """

        sections = language.split("#")
        self.states = sections[0].split(";")
        self.alphabet = sections[1].split(";")
        transitions = sections[2].split(";")
        self.start_state = sections[3].split(";")
        self.accept_states = sections[4].split(";")

        # Parse transitions and build the transition table
        for transition in transitions:
            parts = transition.split(",")
            from_state, symbol, *to_states = parts

            # Initialize nested dict structure if needed
            if from_state not in self.transitions:
                self.transitions[from_state] = {}

            if symbol not in self.transitions[from_state]:
                self.transitions[from_state][symbol] = set()

            # Add destination states to the set for this transition
            self.transitions[from_state][symbol].update(to_states)

    def __str__(self):
        # Pretty-print the NFA structure
        result = []
        result.append("States: " + ", ".join(self.states))
        result.append("Alphabet: " + ", ".join(self.alphabet))
        result.append("Start State: " + ", ".join(self.start_state))
        result.append("Accept States: " + ", ".join(self.accept_states))
        result.append("Transitions:")

        # Format each transition nicely
        for from_state, trans_dict in self.transitions.items():
            for symbol, to_states in trans_dict.items():
                to_states_str = ", ".join(to_states)
                result.append(f"  δ({from_state}, {symbol}) -> {{{to_states_str}}}")

        return "\n".join(result)
