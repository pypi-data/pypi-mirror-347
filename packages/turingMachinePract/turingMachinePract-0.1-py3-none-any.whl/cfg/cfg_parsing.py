import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils")))
from utils import Helper


class CFGParse:
    def __init__(self, grammar):
        self.variables = []
        self.terminals = []
        self.rules = {}
        self.memory = {}  # ? memoization
        self._process_grammar(grammar)
        self.generated_strings = self._generate_strings("S", self.rules, 12)
        print(f"Generated: {self.generated_strings}")

    def is_cfg_ambiguous(self):
        for gene_str in self.generated_strings:
            parse_trees = self._parse_all(gene_str)
            if len(parse_trees) > 1:
                return True
        return False

    def _parse_all(self, gene_str):
        pass

    def _process_grammar(self, grammar):
        # Format: S;T;L#a;b;c;d;i#S/ScTi,La,Ti,b;T/aSb,LabS,i;L/SdL,Si
        sections = grammar.split("#")
        self.variables = sections[0].split(";")
        self.terminals = sections[1].split(";")
        rule_parts = sections[2].split(";")

        for part in rule_parts:
            lhs, rhs = part.split("/")
            self.rules[lhs] = rhs.split(",")

    def _generate_strings(self, start_symbol, rules, max_length=5):
        if max_length == 0:
            return []

        results = set()

        for rule in rules[start_symbol]:
            tokens = Helper.tokenize(rule)  # ? "ab" -> ['a', 'b']

            sub_results = [[]]

            for token in tokens:
                new_sub_result = [[]]
                if token in self.terminals:
                    new_sub_result = [[token]]
                elif token in self.variables:
                    sub_string = self._generate_strings(token, rules, max_length - 1)
                    for ch in sub_string:
                        new_sub_result.append([ch])

                # cross-product
                sub_results = Helper.combine(sub_results, new_sub_result)

            # print(f"Sub Results: {sub_results}")

            for res in sub_results:
                flat = Helper.flatten(res)  # ? [['a'], ['b']] -> ['a', 'b']
                if len(flat) <= max_length and len(flat) > 0:
                    results.add("".join(flat))  # ? 'a', 'b' -> "ab"

        return results

    def __str__(self):
        result = []
        result.append("V: " + ", ".join(self.variables))
        result.append("T: " + ", ".join(self.terminals))
        result.append("R:")
        for variable in self.variables:
            if variable in self.rules:
                productions = " | ".join(self.rules[variable])
                result.append(f"   {variable} -> {productions}")
        return "\n".join(result)
