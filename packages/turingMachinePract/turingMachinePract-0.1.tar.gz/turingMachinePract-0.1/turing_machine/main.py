import sys, os
from turing import TuringMachine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils")))
from utils import Helper


def load_input():
    print(Helper.get_input_explanation("TM"))
    tm = "1111+1111"
    # input("Enter TM in the above Format: ")
    os.system("pause")
    return tm


def main():
    print("================ Turing Machine Inofrmation ================")
    tm_input = load_input()
    Helper.clear_screen()
    tm = TuringMachine(tm_input)
    result = tm.execute()
    print(f"Result: {result}")


if __name__ == "__main__":
    sys.exit(main())
