import sys, os
from nfa_parsing import NFA
from dfa_parsing import DFA

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils")))
from utils import Helper


def load_input():
    print(Helper.get_input_explanation("DFA"))

    nfa = "A;B;C#0;1#A,e,B;B,0,B;B,1,C#A#C"
    # input("Enter NFA in Format: ")
    os.system("pause")
    return nfa


def main():
    nfa_input = load_input()
    Helper.clear_screen()
    nfa_obj = NFA(nfa_input)
    print("================ NFA Inofrmation ================")
    print(nfa_obj)
    print("\n================ DFA Inofrmation ================")
    dfa = DFA(nfa_obj)
    dfa.dfa_equivalence()
    print(dfa)


if __name__ == "__main__":
    sys.exit(main())
