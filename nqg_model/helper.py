def retrieve_prev_state_users(history):
    if len(history) > 1:
        previous_state_users = set(u.label 
                                for u 
                                in history[-1][-1]['users'])
    else:
        previous_state_users = set()
    return previous_state_users