from grammatics import Rule, Grammatics

class Early_Situation:
    '''
    EarlySituation - (left -> right, pointer, link).
    ptr_offset means the position of read index in the self.right string
    '''
    def __init__(self, rule: Rule, pointer_offset = 0, link = 0) -> None:
        self.rule = rule
        self.ptr_offset = pointer_offset
        self.link = link

    def __eq__(self, __value) -> bool:
        return self.rule == __value.rule and \
                        self.ptr_offset == __value.ptr_offset and \
                                self.link == __value.link

    def __repr__(self) -> str:
        return f"{self.rule.left} -> {str(self.rule.right[:self.ptr_offset])} * {str(self.rule.right[self.ptr_offset:])}"

    def __str__(self) -> str:
        return self.__repr__()

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def completed(self) -> bool:
        return self.ptr_offset == len(self.rule.right)

    def get_cur_token(self) -> str:
        return self.rule.right[self.ptr_offset]
    
    def move_offset(self):
        self.ptr_offset = min(self.ptr_offset + 1, len(self.rule.right))

    def copy(self, mv_offset=0):
        return Early_Situation(self.rule, self.ptr_offset + mv_offset, self.link)

class Earley_Parser:
    def __init__(self):
        pass

    def fit(self, grammar: Grammatics):
        grammar.check_grammar()
        self.grammar = grammar

        self.start = "&"
        self.grammar.non_terminals.add(self.start)
        if self.grammar.regym == Grammatics.WORDS:
            self.start_rule = Rule(self.start, self.grammar.start_token)
        elif self.grammar.regym == Grammatics.SENTENCES:
            self.start_rule = Rule(self.start, self.grammar.start_token.split())
        self.rules = {non_term : {Rule(rule.left, rule.right)\
                                    for rule in self.grammar.rules if rule.left == non_term}\
                                                    for non_term in self.grammar.non_terminals}
        self.rules.get(self.start, set()).add(self.start_rule)
        return self

    def predict(self, tokens) -> bool:
        self.situation_sets_list = [set() for _ in range(len(tokens) + 1)]
        self.situation_sets_list[0].add(Early_Situation(self.start_rule))

        check = 0
        while True: # Fisrt step. Fill situation_sets_list[0] set
            check = len(self.situation_sets_list[0])
            self.__complete_situations(0)
            self.__predict_situations(0)
            if check == len(self.situation_sets_list[0]): # Check if set changed
                break

        for index in range(len(tokens)): # First step. Try to read the symbol tokens[index] and fill situation_sets_list[index + 1]
            self.__scan_situations(index + 1, tokens[index])
            while True:
                check = len(self.situation_sets_list[index + 1])
                self.__complete_situations(index + 1)
                self.__predict_situations(index + 1)
                if check == len(self.situation_sets_list[index + 1]):
                    break

        finish_situation = Early_Situation(self.start_rule, 1)
        answer = finish_situation in self.situation_sets_list[-1] # Check the answer
        return answer

    def __scan_situations(self, index: int, token: str):
        for situation in self.situation_sets_list[index - 1]:
            if situation.completed():
                continue
            if situation.get_cur_token() == token:
                self.situation_sets_list[index].add(situation.copy(mv_offset=1))

    def __predict_situations(self, index: int):
        new_situation_set = set()
        for situation in self.situation_sets_list[index]:
            if situation.completed():
                continue
            cur_char = situation.get_cur_token()
            if not cur_char in self.grammar.non_terminals:
                continue
            
            for rule in self.rules[cur_char]:
                new_situation = Early_Situation(rule, link=index)
                new_situation_set.add(new_situation)
        self.situation_sets_list[index].update(new_situation_set)

    def __complete_situations(self, index: int):
        new_situation_set = set()
        for situation in self.situation_sets_list[index]:
            if not situation.completed():
                continue
            for return_trans in self.situation_sets_list[situation.link]:
                if return_trans.completed():
                    continue
                if return_trans.get_cur_token() == situation.rule.left:
                    new_situation_set.add(return_trans.copy(mv_offset=1))
        self.situation_sets_list[index].update(new_situation_set)

if __name__ == '__main__':
    non_terminals = input().split()
    terminals = input().split()

    regym = int(input()) # 0 for parse words and 1 for parse sentences

    rules_number = int(input())
    rules = []
    
    if regym == Grammatics.WORDS:
        for i in range(rules_number):
            rules.append(Rule.parse_rule_symbols(input()))
    elif regym == Grammatics.SENTENCES:
        for i in range(rules_number):
            rules.append(Rule.parse_rule_words(input()))
    else:
        raise RuntimeError("Invalid regym")

    start_token = input()
    if regym == Grammatics.WORDS and len(start_token) != 1:
        raise RuntimeError(f"Invalid start_token '{start_token}'")

    grammar = Grammatics(terminals, non_terminals, start_token, rules, regym)

    early_parser = Earley_Parser()
    early_parser.fit(grammar)

    tokens_number = int(input())
    for i in range(tokens_number):
        if regym == Grammatics.WORDS:
            tokens = input().strip()
        elif regym == Grammatics.SENTENCES:
            tokens = input().strip().split()
        print(early_parser.predict(tokens))
