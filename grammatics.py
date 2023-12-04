class Rule:
    '''Rule - (left -> right) in Grammar'''
    def __init__(self, left: str, right: str, id=0):
        self.id = id
        self.left = left
        self.right = right

    def __eq__(self, __value) -> bool:
        return self.left == __value.left and self.right == __value.right

    def __repr__(self) -> str:
        return f"({self.id}: {self.left}->{self.right})"

    def __str__(self) -> str:
        return self.__repr__()

    def __hash__(self) -> int:
        return hash(self.__repr__())

    @staticmethod
    def parse_rule(string: str):
        rule = string.split("->")
        if len(rule) != 2:
            raise RuntimeError("Правила должны содержать только одну '->', разделяющую правую и левую части.")
        return Rule(rule[0].strip(), rule[1].strip())

class Grammatics:
    def __init__(self, terminals: list, non_terminals: list, start_symbol: str, rules: list):
        self.start_symbol = start_symbol

        self.terminals = set(terminals)
        self.non_terminals = set(non_terminals)

        rules = list(set(rules))
        
        id_cnt = 0
        self.rules = set()
        for rule in rules:
            rule.id = id_cnt
            self.rules.add(rule)
            id_cnt += 1

    def __str__(self) -> str:
        result = "Terminals: " + str(self.terminals) + "\n"
        result += "Nonterminals: " + str(self.non_terminals) + "\n"
        result += "Start symbol: " + self.start_symbol + "\n"
        result += "Number of rules: %d\n" % len(self.rules)
        for rule in self.rules:
            result += str(rule) + "\n"
        return result

    def check_grammar(self):
        if len(self.start_symbol) != 1:
            raise RuntimeError("Стартовый символ {self.start_symbol} должен быть символом.")
        if self.start_symbol not in self.non_terminals:
            raise RuntimeError(f"Стартовый символ {self.start_symbol} должен быть нетерминалом {str(self.non_terminals)}.")
        if len(set(self.terminals) & set(self.non_terminals)) != 0:
            raise RuntimeError(f"Терминалы и нетерминалы не должны пересекаться. В пересечении: {str(set(self.terminals) & set(self.non_terminals))}")
        for rule in self.rules:
            if len(rule.left) != 1 or rule.left not in self.non_terminals:
                raise RuntimeError(f"Левая часть правила {str(rule)} должна быть символом нетерминалом {self.non_terminals}.")
            for symbol in rule.right:
                if symbol not in self.non_terminals and symbol not in self.terminals:
                    raise RuntimeError(f"Cимвол {symbol} в правиле {str(rule)} не является ни терминалом, ни нетерминалом.")

    def get_rule(self, rule_id: int) -> Rule:
        for rule in self.rules:
            if rule.id == rule_id:
                return rule
        return None