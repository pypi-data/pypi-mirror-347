# divisible_by_3_turing_machine/checker.py

states = ["q0", "q1", "q2", "q_accept"]
alpha = ["0", "1"]
tab_alpha = ["0", "1", "_"]
start_state = "q0"
final_states = ["q_accept"]

transition_table = [
    [["q0", "0", "R"], ["q1", "1", "R"], ["q_accept", "_", "S"]],  # q0
    [["q2", "0", "R"], ["q0", "1", "R"], "-"],  # q1
    [["q1", "0", "R"], ["q2", "1", "R"], "-"],  # q2
]

def check_divisable_by_3(binary_num):
    """
    A Turing machine that checks if a binary number is divisible by 3.

    Parameters:
        binary_num (str): A binary number represented as a string (e.g., "101").

    Returns:
        bool: True if the number is divisible by 3, False otherwise.
    """
    tab_str = "_" + binary_num + "_"
    tab_list = list(tab_str)
    head = 1
    next_state = ""
    index = 0
    while True:

        if index == 0:
            state_index = states.index(start_state)
        else:
            state_index = states.index(next_state)

        char_index = tab_alpha.index(tab_list[head])

        transition = transition_table[state_index][char_index]

        if transition == "-":
            return False

        next_state = transition[0]
        tab_list[head] = transition[1]

        if transition[2] == 'L':
            head -= 1
        elif transition[2] == 'R':
            head += 1

        if next_state in final_states:
            return True
        index += 1
