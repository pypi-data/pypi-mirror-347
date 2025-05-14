

states = ["q0", "q1", "q2", "q3"]
start_state = "q0"
final_states = ["q3"]
alpha = ["0", "1"]
transition_table = [
    ["q0", "q1"],
    ["q2", "q1"],
    ["q0", "q3"],
    ["q3", "q3"]
]

def check_accept_of_str(string):
    """
    Check if the given binary string is accepted by the DFA that accepts strings containing '101'.

    Parameters:
        string (str): The binary string to check (e.g., '101011').

    Returns:
        bool: True if the string is accepted, False otherwise.
    """
    next_state = ''
    for index, char in enumerate(string):
        if index == 0:
            state_index = states.index(start_state)
        else:
            state_index = states.index(next_state)

        char_index = alpha.index(char)
        next_state = transition_table[state_index][char_index]

    return next_state in final_states
