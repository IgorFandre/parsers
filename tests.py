from grammatics import Grammatics, Rule
from early_parser import Earley_Parser
import json
import random

COCKE_TEST_NUMBER = 3
EARLY_TEST_NUMBER = 4
GENERAL_TEST_NUMBER = 2

def test_Early_algorithm():
    for i in range(GENERAL_TEST_NUMBER):
        with open('tests/General/' + str(i + 1) + '.json', 'r') as test_file:
            print('tests/General/' + str(i + 1) + '.json')
            non_terminals = set(["S", "A", "B", "C", "D", "F"])
            terminals = set(["a", "b", "c", "(", ")"])
            test_data = json.load(test_file)
            rule_list = []
            for rule_str in test_data['rules']:
                rule_list.append(Rule.parse_rule(rule_str))
            grammar = Grammatics(terminals, non_terminals, "S", rule_list)
            early = Earley_Parser().fit(grammar)
            for j in range(len(test_data['words'])):
                ans = early.predict(test_data['words'][j])
                real_ans = test_data['answers'][j]
                assert ans == real_ans, "word: %s, General grammar test number: %d" % (test_data['words'][j], i + 1)

    for i in range(COCKE_TEST_NUMBER):
        with open('tests/CockeYoungerKasami/' + str(i + 1) + '.json', 'r') as test_file:
            non_terminals = set(["S", "A", "B", "C", "F", "D", "E", "X", "Y", "K", "L", "M"])
            terminals = set(["a", "b", "c", "(", ")"])
            test_data = json.load(test_file)
            rule_list = []
            for rule_str in test_data['rules']:
                rule_list.append(Rule.parse_rule(rule_str))
            grammar = Grammatics(terminals, non_terminals, "S", rule_list)
            early = Earley_Parser().fit(grammar)
            for j in range(len(test_data['words'])):
                ans = early.predict(test_data['words'][j])
                real_ans = test_data['answers'][j]
                assert ans == real_ans, "word: %s, CockeYoungerKasami grammar test number: %d" % (test_data['words'][j], i + 1)

    for i in range(EARLY_TEST_NUMBER):
        with open('tests/Early/' + str(i + 1) + '.json', 'r') as test_file:
            non_terminals = set(["S", "A", "B", "C", "F"])
            terminals = set(["a", "b", "c", "(", ")"])
            test_data = json.load(test_file)
            rule_list = []
            for rule_str in test_data['rules']:
                rule_list.append(Rule.parse_rule(rule_str))
            grammar = Grammatics(terminals, non_terminals, "S", rule_list)
            early = Earley_Parser().fit(grammar)
            for j in range(len(test_data['words'])):
                ans = early.predict(test_data['words'][j])
                real_ans = test_data['answers'][j]
                assert ans == real_ans, "word: %s, Early grammar test number: %d" % (test_data['words'][j], i + 1)

