import unittest
from finite_state_automaton import FiniteStateAutomaton as FSM


class FSMTestCase(unittest.TestCase):

    def test_FSM1(self):
        m = FSM()
        m.alphabet = {'0', '1'}
        m.states = {'A'}
        m.initial_state = 'A'
        m.final_states = {'A'}
        m.transitions = {('A', '1'): {'A'}}
        # m.draw('fsm1')

        self.assertTrue(m.is_accepted('1'))
        self.assertTrue(m.is_accepted('1 1 1 1'))
        self.assertFalse(m.is_accepted('0'))
        self.assertFalse(m.is_accepted('0 0 0 0'))

    def test_FSM2(self):
        m = FSM()
        m.alphabet = {'0', '1'}
        m.states = {'A', 'B', 'C'}
        m.initial_state = 'A'
        m.final_states = {'C'}
        m.transitions = {('A', '0'): {'A', 'B'}, ('A', '1'): {'B'}, ('B', '0'): {'C'}, ('B', '1'): {'A'}, ('C', '1'): {'C'}}
        # m.draw('fsm2')

        self.assertTrue(m.is_accepted('0 0'))
        self.assertTrue(m.is_accepted('1 0'))
        self.assertTrue(m.is_accepted('1 0 1'))
        self.assertTrue(m.is_accepted('0 0 1 1 1 1'))
        self.assertTrue(m.is_accepted('1 1 0 0'))
        self.assertTrue(m.is_accepted('0 1 0 1 0 1 0'))
        self.assertTrue(m.is_accepted('0 1 0 1 0 1 1'))
        self.assertTrue(m.is_accepted('0 0 0 0 1 0 0 0 1 0 1 0 1 1'))

        self.assertFalse(m.is_accepted('1'))
        self.assertFalse(m.is_accepted('0'))
        self.assertFalse(m.is_accepted('1 1'))
        self.assertFalse(m.is_accepted('1 1 1 1 1 1 1'))

    def test_next_states(self):
        m = FSM()
        m.alphabet = {'0', '1'}
        m.states = {'A', 'B', 'C'}
        m.initial_state = 'A'
        m.final_states = {'C'}
        m.transitions = {('A', '0'): {'A', 'B'}, ('A', '1'): {'B'}, ('B', '0'): {'A', 'B', 'C'}}

        self.assertEqual(m.next_states('A'), {'A', 'B'})
        self.assertEqual(m.next_states('B'), {'A', 'B', 'C'})
        self.assertEqual(m.next_states('C'), set())
