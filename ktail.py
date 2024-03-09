from natsort import natsorted
from finite_state_automaton import FiniteStateAutomaton as FSM
from typing import Set, Tuple, List

initial_symbol = '$'
final_symbol = '#'


def rename_states(m: FSM, prefix: str = 'q') -> FSM:
    """Return a new FSM with all states renamed with the given prefix.

    :param m: FSM
    :param prefix: prefix for the new state names
    :return: a new FSM with renamed states
    """
    # initialise a new FSM
    m_new = FSM()

    # copy the alphabet (should not change)
    m_new.alphabet = m.alphabet

    # rename the initial state
    rename = dict()
    rename[m.initial_state] = f'{prefix}0'
    m_new.states.add(rename[m.initial_state])
    m_new.initial_state = rename[m.initial_state]

    # rename the other states (depth-first ordering)
    # NOTE: unreachable states will not be included in the new FSM!
    i = 1
    working_states = [m.initial_state]
    while working_states:
        curr_state = working_states.pop()
        for next_state in natsorted(m.next_states(curr_state)):
            if next_state not in rename.keys():
                rename[next_state] = f'{prefix}{i}'
                m_new.states.add(rename[next_state])
                working_states.insert(0, next_state)
                i += 1

    # update the transitions and final states
    for (curr_state, label), next_states in m.transitions.items():
        m_new.transitions[(rename[curr_state], label)] = {rename[next_state] for next_state in next_states}
    m_new.final_states = {rename[state] for state in m.final_states}

    # print rename dictionary
    print('Renaming dictionary:')
    for key, value in rename.items():
        print(key, '->', value)

    return m_new


def generate_PTA(words: List[str], sep=' ', draw_PTA=False) -> FSM:
    """Generate a PTA from the given set of words.
    Note that it uses special symbols for the initial and final states.

    :param words: set of words
    :param sep: separator between symbols in the words (default: whitespace)
    :param draw_PTA: whether to draw the PTA (default: False)
    :return: PTA
    """

    # initialise an empty FSM
    m = FSM()

    # set the initial state
    m.initial_state = '_INIT_'
    m.states.add(m.initial_state)

    # add special symbols to the alphabet
    assert initial_symbol not in m.alphabet
    m.alphabet.add(initial_symbol)
    assert final_symbol not in m.alphabet
    m.alphabet.add(final_symbol)

    # For each word, we will create a linear chain of states to accept it.
    state_counter = 1
    for word in words:
        # convert whitespace-separated word to a sequence of events
        word = word.split(sep=sep)

        assert len(word) > 0
        first_state = f's{state_counter}'  # the first state for the given word
        m.states.add(first_state)
        state_counter += 1

        # add the epsilon transition (with the special initial symbol) from the initial state to the first state
        m.transitions.setdefault((m.initial_state, initial_symbol), set()).add(first_state)

        # append a state and a transition for each symbol in the word
        current_state = first_state
        for i in range(len(word)):
            # get the i-th symbol
            symbol = word[i]

            # update the FSM
            m.alphabet.add(symbol)
            next_state = f's{state_counter}'
            m.states.add(next_state)
            m.transitions.setdefault((current_state, symbol), set()).add(next_state)
            state_counter += 1

            # update the current state
            current_state = next_state

        # For each word, the last state is a final state.
        # We need to add a special final state and a transition from the last state to the special final state.
        # This is just to make the remaining computation easier.
        special_final_state = '_FINAL_'
        m.states.add(special_final_state)
        m.final_states.add(special_final_state)
        m.transitions.setdefault((current_state, final_symbol), set()).add(special_final_state)

    if draw_PTA:
        m.draw('PTA')

    return m


def get_k_future(m: FSM, k: int, curr_state: str, print_futures=False) -> Set[Tuple[str, ...]]:
    """Return the set of consecutive sequences of k future events or less starting from the given state.

    :param m: FSM
    :param k: maximum length of the future sequences
    :param curr_state: current state
    :param print_futures: whether to print the future sequences
    :return: set of k-sequences (future event sequences with length up to k)
    """
    assert k > 0

    if k == 1:
        # base case
        futures = {tuple({symbol}) for symbol in m.alphabet if (curr_state, symbol) in m.transitions.keys()}
        if print_futures:
            print(f'k={k}, curr_state={curr_state}, futures={futures}')
        return futures
    else:
        # recursive case
        futures = get_k_future(m, k - 1, curr_state)  # futures of exactly k-1 length from the current state
        for symbol in m.alphabet:
            if (curr_state, symbol) in m.transitions.keys():
                next_states = m.transitions[(curr_state, symbol)]
                for next_state in next_states:
                    futures |= {tuple({symbol}) + suffix for suffix in get_k_future(m, k - 1, next_state)}
        if print_futures:
            print(f'k={k}, curr_state={curr_state}, futures={futures}')
        return futures


def k_future_mapping(m: FSM, k: int, print_map=False) -> dict:
    """Return the future map for the given FSM and k.

    :param m: FSM
    :param k: maximum length of the future sequences
    :param print_map: whether to print the future map (default: False)
    :return: future map
    """
    future_map = dict()

    # for each state, we will find the futures and add them to the future map's keys.
    # at the same time, we will map the futures of the next states to the future map's values.
    for curr_state in m.states:
        next_states = m.next_states(curr_state)
        for next_state in next_states:
            future_curr = frozenset(get_k_future(m, k, curr_state))
            future_next = frozenset(get_k_future(m, k, next_state))
            future_map.setdefault(future_curr, set()).add(future_next)

    # print the future map if needed
    if print_map:
        print('-' * 50)
        print('Future map:')
        for future_src in future_map.keys():
            print(f'{future_src} -> {future_map[future_src]}')
        print('-' * 50)

    return future_map


def infer_model(future_map: dict, draw_inferred_model=False) -> FSM:
    """Infer a model from the future map.
    It assumes there are special initial and final symbols used in the PTA generation step.
    They are essential to identify the initial and final states from the future map.

    :param future_map: future map
    :param draw_inferred_model: whether to draw the inferred model (default: False)
    :return: inferred model
    """
    m = FSM()

    # each set of k-sequences in the future map (both key and value) is a (merged) state in the inferred model
    for future_src in future_map.keys():
        m.states.add(str(future_src))

        # the first symbol of the k-sequences (of the current state) is the label of the transition
        # note that all the k-sequences in the future map have the same first symbol by design
        label = tuple(future_src)[0][0]
        m.alphabet.add(label)

        # the set of k-sequences is the initial state if it is the source of the special initial symbol
        if label == initial_symbol:
            m.initial_state = str(future_src)

        # process each of the next states' k-sequences in the future map
        for future_dst in future_map[future_src]:
            m.states.add(str(future_dst))
            m.transitions.setdefault((str(future_src), label), set()).add(str(future_dst))

            # the set of k-sequences is the final state if it is the target of the special final symbol
            if label == final_symbol:
                m.final_states.add(str(future_dst))

    # draw the inferred model if needed
    if draw_inferred_model:
        m.draw('inferred-model')

    # return the inferred model
    return m


def ktail(words: List[str], k: int, sep=' ', shorten_state_names=True, print_internals=False) -> FSM:
    """The k-tail algorithm that infers a model from a set of words and a given k.

    :param words: list of words (each word is a whitespace-separated sequence of symbols by default)
    :param k: the parameter k
    :param sep: separator between symbols in the words (default: whitespace)
    :param shorten_state_names: whether to shorten state names (default: True)
    :param print_internals: whether to print the internal steps (default: False)
    :return: inferred model
    """

    # Step1: Generate a PTA from the given set of words
    m = generate_PTA(words, sep=sep, draw_PTA=print_internals)

    # (optional) print the future k-sequences for each state and the k-equivalent classes
    if print_internals:
        print('Future k-sequences:')
        for state in natsorted(m.states):
            print(f'future_{k}({state}) = {get_k_future(m, k, state)}')
        print('-' * 50)

        equivalent_classes = dict()
        for state in m.states:
            equivalent_classes.setdefault(frozenset(get_k_future(m, k, state)), set()).add(state)
        print('Equivalent classes:')
        for k_seq, states in equivalent_classes.items():
            print(f'{k_seq} -> {natsorted(states)}')

    # Step2: Compute the future map from the PTA
    future_map = k_future_mapping(m, k, print_map=print_internals)

    # Step3: Infer the model from the future map
    m_k = infer_model(future_map)

    # (optional) shorten the state names if needed
    if shorten_state_names:
        m_k = rename_states(m_k)

    return m_k


if __name__ == '__main__':
    k = 2
    words = [
        'a b',
        'a b b',
        'a b b b'
    ]
    m = ktail(words=words, k=k, sep=' ', print_internals=False)
    m.draw(f'{k}-tail-result')
