from typing import Set, Dict


class FiniteStateAutomaton:
    alphabet: Set[str]
    states: Set[str]
    initial_state: str
    final_states: Set[str]
    transitions: Dict  # (state, symbol) -> Set of states

    def __init__(self):
        self.alphabet = set()
        self.states = set()
        self.final_states = set()
        self.transitions = dict()
        self.initial_state = ''

    def next_states(self, state):
        """Return all possible next states from a given state.

        :param state: current state
        :return: a set of next states
        """
        next_states = set()
        for (s, symbol) in self.transitions.keys():
            if s == state:
                next_states |= self.transitions[(s, symbol)]
        return next_states

    def is_accepted(self, word):
        """Check if a word is accepted by the FSM.

        :param word: input word
        :return: True if the word is accepted, False otherwise
        """
        current_states = [self.initial_state]
        for symbol in word:
            next_states = set()
            for state in current_states:
                if (state, symbol) in self.transitions.keys():
                    next_states |= self.transitions[(state, symbol)]
            current_states = next_states
        return any(state in self.final_states for state in current_states)

    def draw(self, name='fsm'):
        import graphviz
        dot = graphviz.Digraph('finite_state_machine', filename=f'{name}.gv')
        dot.attr(rankdir='LR', size='8,5')

        # add a dummy state to make the initial state an actual state
        dot.node('start', shape='point')
        dot.edge('start', self.initial_state)

        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)
        for (state, symbol), next_states in self.transitions.items():
            for next_state in next_states:
                dot.edge(state, next_state, label=symbol)

        dot.view(name)

    def __str__(self):
        return f'Alphabet: {self.alphabet}\n' \
               f'States: {self.states}\n' \
               f'Initial state: {self.initial_state}\n' \
               f'Final states: {self.final_states}\n' \
               f'Transitions: {self.transitions}'
