from grammatics import Grammatics, Rule
from early_parser import Earley_Parser
from lr1_parser import LR1_Parser
import json

COCKE_TEST_NUMBER = 3
EARLY_TEST_NUMBER = 4
LR1_TEST_NUMBER = 2
GENERAL_TEST_NUMBER = 2
SENTENCES_TEST_NUMBER = 3

def parse_simple_grammar_file(test_data) -> Grammatics:
    non_terminals = set(["S", "A", "B", "C", "D", "F", "E", "X", "Y", "K", "L", "M"])
    terminals = set(["a", "b", "c", "d", "(", ")"])

    regym = Grammatics.WORDS if test_data["regym"] == "WORDS" else Grammatics.SENTENCES

    rule_list = []
    if regym == Grammatics.WORDS:
        for rule_str in test_data['rules']:
            rule_list.append(Rule.parse_rule_symbols(rule_str))
    elif regym == Grammatics.SENTENCES:
        for rule_str in test_data['rules']:
            rule_list.append(Rule.parse_rule_words(rule_str))

    return Grammatics(terminals, non_terminals, "S", rule_list, regym)

def test_Early_algorithm():
    for i in range(GENERAL_TEST_NUMBER):
        with open('tests/General/' + str(i + 1) + '.json', 'r') as test_file:
            print('tests/General/' + str(i + 1) + '.json')

            test_data = json.load(test_file)

            grammar = parse_simple_grammar_file(test_data)
            parser = Earley_Parser().fit(grammar)

            for j in range(len(test_data['words'])):
                ans = parser.predict(test_data['words'][j])
                real_ans = test_data['answers'][j]
                assert ans == real_ans, "word: %s, General grammar test number: %d" % (test_data['words'][j], i + 1)

    for i in range(COCKE_TEST_NUMBER):
        with open('tests/CockeYoungerKasami/' + str(i + 1) + '.json', 'r') as test_file:
            print('tests/CockeYoungerKasami/' + str(i + 1) + '.json')

            test_data = json.load(test_file)

            grammar = parse_simple_grammar_file(test_data)
            parser = Earley_Parser().fit(grammar)

            for j in range(len(test_data['words'])):
                ans = parser.predict(test_data['words'][j])
                real_ans = test_data['answers'][j]
                assert ans == real_ans, "word: %s, CockeYoungerKasami grammar test number: %d" % (test_data['words'][j], i + 1)

    for i in range(EARLY_TEST_NUMBER):
        with open('tests/Early/' + str(i + 1) + '.json', 'r') as test_file:
            print('tests/Early/' + str(i + 1) + '.json')

            test_data = json.load(test_file)

            grammar = parse_simple_grammar_file(test_data)
            parser = Earley_Parser().fit(grammar)

            for j in range(len(test_data['words'])):
                ans = parser.predict(test_data['words'][j])
                real_ans = test_data['answers'][j]
                assert ans == real_ans, "word: %s, Early grammar test number: %d" % (test_data['words'][j], i + 1)
    
    for i in range(SENTENCES_TEST_NUMBER):
        with open('tests/Sentences/' + str(i + 1) + '.json', 'r') as test_file:
            print('tests/Sentences/' + str(i + 1) + '.json')

            test_data = json.load(test_file)

            non_terminals = set(test_data["non_terminals"])
            terminals = set(test_data["terminals"])

            regym = Grammatics.WORDS if test_data["regym"] == "WORDS" else Grammatics.SENTENCES

            rule_list = []
            if regym == Grammatics.WORDS:
                for rule_str in test_data['rules']:
                    rule_list.append(Rule.parse_rule_symbols(rule_str))
            elif regym == Grammatics.SENTENCES:
                for rule_str in test_data['rules']:
                    rule_list.append(Rule.parse_rule_words(rule_str))

            grammar = Grammatics(terminals, non_terminals, test_data["start"], rule_list, regym)
            parser = Earley_Parser().fit(grammar)

            for j in range(len(test_data['words'])):
                ans = parser.predict(test_data['words'][j].strip().split())
                real_ans = test_data['answers'][j]
                assert ans == real_ans, "word: %s, Sentences grammar test number: %d" % (test_data['words'][j], i + 1)

def test_LR1_algorithm():
    for i in range(GENERAL_TEST_NUMBER):
        with open('tests/General/' + str(i + 1) + '.json', 'r') as test_file:
            print('tests/General/' + str(i + 1) + '.json')

            test_data = json.load(test_file)

            grammar = parse_simple_grammar_file(test_data)
            parser = LR1_Parser().fit(grammar)

            for j in range(len(test_data['words'])):
                ans = parser.predict(test_data['words'][j])
                real_ans = test_data['answers'][j]
                assert ans == real_ans, "word: %s, General grammar test number: %d" % (test_data['words'][j], i + 1)

    for i in range(LR1_TEST_NUMBER):
        with open('tests/LR1/' + str(i + 1) + '.json', 'r') as test_file:
            print('tests/LR1/' + str(i + 1) + '.json')

            test_data = json.load(test_file)

            grammar = parse_simple_grammar_file(test_data)
            parser = LR1_Parser().fit(grammar)

            for j in range(len(test_data['words'])):
                ans = parser.predict(test_data['words'][j])
                real_ans = test_data['answers'][j]
                assert ans == real_ans, "word: %s, LR1 grammar test number: %d" % (test_data['words'][j], i + 1)

    for i in range(SENTENCES_TEST_NUMBER):
        with open('tests/Sentences/' + str(i + 1) + '.json', 'r') as test_file:
            print('tests/Sentences/' + str(i + 1) + '.json')

            test_data = json.load(test_file)

            non_terminals = set(test_data["non_terminals"])
            terminals = set(test_data["terminals"])

            regym = Grammatics.WORDS if test_data["regym"] == "WORDS" else Grammatics.SENTENCES

            rule_list = []
            if regym == Grammatics.WORDS:
                for rule_str in test_data['rules']:
                    rule_list.append(Rule.parse_rule_symbols(rule_str))
            elif regym == Grammatics.SENTENCES:
                for rule_str in test_data['rules']:
                    rule_list.append(Rule.parse_rule_words(rule_str))

            grammar = Grammatics(terminals, non_terminals, test_data["start"], rule_list, regym)
            parser = LR1_Parser().fit(grammar)

            for j in range(len(test_data['words'])):
                ans = parser.predict(test_data['words'][j].strip().split())
                real_ans = test_data['answers'][j]
                assert ans == real_ans, "word: %s, Sentences grammar test number: %d" % (test_data['words'][j], i + 1)
