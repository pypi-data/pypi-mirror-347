def is_anbn(s):
    """
    Simulates a PDA to check if a string is accepted by the language a^n b^n (n >= 0).
    Returns True if accepted, False otherwise.
    """
    stack = []
    i = 0
    n = len(s)

    # Push 'A' for each 'a'
    while i < n and s[i] == 'a':
        stack.append('A')
        i += 1

    # Pop for each 'b'
    while i < n and s[i] == 'b':
        if not stack:
            return False  # More 'b's than 'a's
        stack.pop()
        i += 1

    # If stack is empty and all input is consumed, accept
    return not stack and i == n
