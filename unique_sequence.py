def minimal_rotation(s):
    """Return the lexicographically smallest rotation of string s."""
    return min(s[i:] + s[:i] for i in range(len(s)))

def find_unique_sequences_v5(ListOfSequence):
    unique_sequence = []
    seen_rotations = set()

    for binary_sequence in ListOfSequence:
        sequence = binary_sequence[0]
        min_rot = minimal_rotation(sequence)
        if min_rot not in seen_rotations:
            unique_sequence.append(binary_sequence)
            seen_rotations.add(min_rot)

    return unique_sequence