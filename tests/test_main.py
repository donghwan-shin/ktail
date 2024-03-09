import unittest

from finite_state_automaton import FiniteStateAutomaton as FSM
from ktail import generate_PTA, get_k_future, k_future_mapping, rename_states, ktail


class TestMain(unittest.TestCase):
    def test_generate_PTA(self):
        words = [
            'a b c d',
            'a b c e'
        ]
        m = generate_PTA(words)
        self.assertEqual(m.alphabet, {'a', 'b', 'c', 'd', 'e', '$', '#'})
        self.assertEqual(m.states, {'_INIT_', '_FINAL_', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10'})
        self.assertEqual(m.initial_state, '_INIT_')
        self.assertEqual(m.final_states, {'_FINAL_'})
        self.assertEqual(m.transitions, {('_INIT_', '$'): {'s6', 's1'}, ('s1', 'a'): {'s2'},
                                         ('s2', 'b'): {'s3'}, ('s3', 'c'): {'s4'}, ('s4', 'd'): {'s5'},
                                         ('s6', 'a'): {'s7'}, ('s7', 'b'): {'s8'}, ('s8', 'c'): {'s9'},
                                         ('s9', 'e'): {'s10'},  ('s5', '#'): {'_FINAL_'},  ('s10', '#'): {'_FINAL_'}})
        # m.draw('PTA-test')

    def test_get_k_future(self):
        m = FSM()
        m.alphabet = {'ax', 'bx', 'cx', 'dx', 'ex'}
        m.states = {'s1', 's2', 's3', 's4', 's5', 's6'}
        m.initial_state = 's1'
        m.final_states = {'s4', 's6'}
        m.transitions = {
            ('s1', 'ax'): {'s2', 's5'},
            ('s2', 'bx'): {'s3'},
            ('s3', 'cx'): {'s4'},
            ('s5', 'dx'): {'s5'},
            ('s5', 'ex'): {'s6'}
        }
        # self.assertEqual(get_k_future(m, 1, 's1'), {('ax',)})
        self.assertEqual(get_k_future(m, 2, 's1'), {('ax',), ('ax', 'bx'), ('ax', 'dx'), ('ax', 'ex')})
        self.assertEqual(get_k_future(m, 3, 's1'),
                         {('ax',),
                          ('ax', 'bx'), ('ax', 'dx'), ('ax', 'ex'),
                          ('ax', 'bx', 'cx'), ('ax', 'dx', 'dx'), ('ax', 'dx', 'ex')})
        self.assertEqual(get_k_future(m, 4, 's1'),
                         {('ax',),
                          ('ax', 'bx'), ('ax', 'dx'), ('ax', 'ex'),
                          ('ax', 'bx', 'cx'), ('ax', 'dx', 'dx'), ('ax', 'dx', 'ex'),
                          ('ax', 'dx', 'dx', 'ex'), ('ax', 'dx', 'dx', 'dx')})
        self.assertEqual(get_k_future(m, 3, 's5'),
                         {('dx',), ('ex',), ('dx', 'dx'), ('dx', 'ex'), ('dx', 'dx', 'dx'), ('dx', 'dx', 'ex')})
        self.assertEqual(get_k_future(m, 1, 's3'), {('cx',)})
        self.assertEqual(get_k_future(m, 2, 's3'), {('cx',)})
        self.assertEqual(get_k_future(m, 1, 's4'), set())

    def test_k_future_mapping(self):
        m = FSM()
        m.alphabet = {'$', '0', '1', '#'}
        m.states = {f'q{i}' for i in range(11)}
        m.initial_state = 'q0'
        m.final_states = {'q10'}
        m.transitions = {
            ('q0', '$'): {'q1', 'q3', 'q6'},
            ('q1', '1'): {'q2'},
            ('q3', '0'): {'q4'},
            ('q4', '1'): {'q5'},
            ('q6', '0'): {'q7'},
            ('q7', '0'): {'q8'},
            ('q8', '1'): {'q9'},
            ('q2', '#'): {'q10'},
            ('q5', '#'): {'q10'},
            ('q9', '#'): {'q10'}
        }
        # m.draw()
        future_map = k_future_mapping(m, 1)
        for (k, v) in future_map.items():
            print(f'{k} -> {v}')
        self.assertEqual(future_map, {
            frozenset({('1',)}): {frozenset({('#',)})},
            frozenset({('0',)}): {frozenset({('1',)}), frozenset({('0',)})},
            frozenset({('#',)}): {frozenset()},
            frozenset({('$',)}): {frozenset({('1',)}), frozenset({('0',)})}})

    def test_rename_states(self):
        m = FSM()
        m.alphabet = {'e', '0', '1'}
        m.states = {f's{i}' for i in range(10)}
        m.initial_state = 's0'
        m.final_states = {'s2', 's5', 's9'}
        m.transitions = {
            ('s0', 'e'): {'s1', 's3', 's6'},
            ('s1', '1'): {'s2'},
            ('s3', '0'): {'s4'},
            ('s4', '1'): {'s5'},
            ('s6', '0'): {'s7'},
            ('s7', '0'): {'s8'},
            ('s8', '1'): {'s9'},
        }
        m_new = rename_states(m, 'q')
        self.assertEqual(m_new.alphabet, m.alphabet)
        self.assertEqual(m_new.initial_state, 'q0')
        self.assertEqual(m_new.final_states, {'q4', 'q7', 'q9'})
        self.assertEqual(m_new.states, {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9'})
        self.assertEqual(
            m_new.transitions,
            {('q0', 'e'): {'q2', 'q1', 'q3'},
             ('q1', '1'): {'q4'},
             ('q2', '0'): {'q5'},
             ('q3', '0'): {'q6'},
             ('q5', '1'): {'q7'},
             ('q6', '0'): {'q8'},
             ('q8', '1'): {'q9'}}
        )

    def test_infer_model(self):
        pass  # FIXME

    def test_ktail(self):
        k = 2
        words = [
            'a b c',
            'a b d',
            'a b e'
        ]
        m = ktail(words=words, k=k)
        self.assertEqual({'a', 'e', '#', 'b', '$', 'c', 'd'}, m.alphabet)
        self.assertEqual({'q7', 'q5', 'q2', 'q3', 'q6', 'q8', 'q0', 'q9', 'q1', 'q4'}, m.states)
        self.assertEqual('q0', m.initial_state)
        self.assertEqual({'q9'}, m.final_states)
        self.assertEqual(True, m.is_accepted('$ a b c #'))
        self.assertEqual(True, m.is_accepted('$ a b d #'))
        self.assertEqual(True, m.is_accepted('$ a b e #'))
        self.assertEqual(False, m.is_accepted('a b c'))

    def test_ktail2(self):
        k = 1
        words = [
            'hello world',
            'hello hello world'
        ]
        m = ktail(words=words, k=k)
        self.assertTrue(m.is_accepted("$ hello world #"))
        self.assertTrue(m.is_accepted("$ hello hello world #"))
        self.assertTrue(m.is_accepted("$ hello hello hello hello hello world #"))
