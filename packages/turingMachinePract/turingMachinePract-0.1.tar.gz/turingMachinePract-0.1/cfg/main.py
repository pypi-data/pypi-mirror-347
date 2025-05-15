import sys, os
from cfg_parsing import CFGParse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils")))
from utils import Helper


def load_input():
    print(Helper.get_input_explanation("CFG"))
    cfg = input("Enter your CFG: ").strip()
    return cfg


# * Tests:
# S;T;L#a;b;c;d;i#S/ScTi,La,Ti,b;T/aSb,LabS,i;L/SdL,Si
# S;A#a;b#S/aSb,A;A/ab,e


def main():
    cfg_input = load_input()
    Helper.clear_screen()
    cfg_parse = CFGParse(cfg_input)
    print(cfg_parse)


if __name__ == "__main__":
    sys.exit(main())
