import os


class Helper:

    @staticmethod
    def get_input_explanation(problem):
        if problem == "CFG":
            return """
            === Context-Free Grammar (CFG) Definition ===
            A CFG is defined as a 4-tuple (V, Σ, R, S) where:
                1. V: A finite set of variables (non-terminals)
                2. Σ: A finite set of terminals (symbols in the alphabet)
                3. R: A finite set of production rules
                4. S: A start variable, where S ∈ V

            === Input Format ===
            Please enter the CFG in the following format:  V1;V2;...#t1;t2;...#LHS1/RHS1,RHS2;LHS2/RHS1,...
            Where:
                - V1;V2;... : semicolon-separated variables (non-terminals)
                - t1;t2;... : semicolon-separated terminals
                - Rules: Each rule set is of the form LHS/productions (comma-separated)

            Example input:
                S;T;L#a;b;c;d;i#S/ScTi,La,Ti,b;T/aSb,LabS,i;L/SdL,Si
            """
        elif problem == "DFA":
            return """
        === Nondeterministic Finite Automaton (NFA) Definition ===
        A NFA is defined as a 5-tuple (Q, Σ, δ, q0, F), where:
            1. Q: A finite set of states.")
            2. Σ (Sigma): A finite set called the alphabet (input symbols).
            3. δ (delta): The transition function δ: Q × Σε → P(Q), mapping a state and input to a set of states.
            4. q0: The start state, which must be a member of Q.
            5. F: The set of accept (final) states, a subset of Q.

            === Input Format ===
            Enter the NFA in the following format: states#alphabet#transitions#start_state#accept_states
            where:
                - states: semicolon-separated (e.g., q0;q1;q2)")
                - alphabet: semicolon-separated (e.g., a;b)")
                - transitions: semicolon-separated; each is state,symbol,next1,next2,...
                - start_state: a single state (e.g., q0)
                - accept_states: comma-separated (e.g., q2,q3)

            Example input:
                q0;q1;q2;q3#a;b#q0,a,q1,q2;q1,e,q1,q3;q0,b,q3#q0#q2,q3
        """
        elif problem == "TM":
            return """Turing Machine for Unary Addition
            Given an input of the form: 111+11
            Reads all 1s until it finds +,
            Replaces + with 1 (combining numbers),
            Continues to the end of the tape,
            Moves left to the last 1 and replaces it with B,
            Ends execution in the accept state"""
        else:
            return "Please, Enter the name of the problem..."

    @staticmethod
    def combine(list1, list2):  # ? cross-product between two lists of lists.
        result = []
        for l1 in list1:
            for l2 in list2:
                result.append(l1 + l2)
        return result

    @staticmethod
    def flatten(lst):
        flattened_list = []
        for sublist in lst:
            for item in sublist:
                flattened_list.append(item)
        return flattened_list

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def tokenize(production):  # ? 'aSb' -> ['a', 'S', 'b']
        return list(production)
