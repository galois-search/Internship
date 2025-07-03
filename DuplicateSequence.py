def find_unique_sequences_v4(ListOfSequence):
    unique_sequence = []
    duplicate_sequence = []
    for binary_sequence in ListOfSequence:
        sequence = binary_sequence[0]
        if sequence in unique_sequence:
            duplicate_sequence.append(binary_sequence)
        else:
            current_sequence = sequence
            shifted_sequence = ""
            while shifted_sequence != sequence:
                shifted_sequence = current_sequence[1:] + current_sequence[0]
                if any(shifted_sequence in tup for tup in unique_sequence):
                    duplicate_sequence.append(binary_sequence)
                else:
                    current_sequence = shifted_sequence

            if shifted_sequence == sequence and not any(sequence in tup for tup in unique_sequence):
                unique_sequence.append(binary_sequence)

    return unique_sequence,duplicate_sequence

def minimal_rotation(s):
    """Return the lexicographically smallest rotation of string s."""
    return min(s[i:] + s[:i] for i in range(len(s)))

def is_rotation(original, candidate):
    return len(original) == len(candidate) and candidate in (original + original)

def find_unique_sequences_v5(ListOfSequence):
    unique_sequence = []
    duplicate_sequence1 = []
    duplicate_sequence2 = []
    seen_rotations = set()

    for binary_sequence in ListOfSequence:
        sequence = binary_sequence[0]
        min_rot = minimal_rotation(sequence)
        if min_rot in seen_rotations :
            if is_rotation(min_rot,unique_sequence[0][0]):
                duplicate_sequence1.append(binary_sequence)
            else:
                duplicate_sequence2.append(binary_sequence)
        else:
            unique_sequence.append(binary_sequence)
            seen_rotations.add(min_rot)

    return unique_sequence, duplicate_sequence1,duplicate_sequence2


import os

def group_duplicates_by_original(ListOfSequence):
    unique_map = {}  # minimal_rotation -> (original_sequence, [duplicates])
    for binary_sequence in ListOfSequence:
        sequence = binary_sequence[0]
        min_rot = minimal_rotation(sequence)
        if min_rot in unique_map:
            unique_map[min_rot][1].append(binary_sequence)
        else:
            unique_map[min_rot] = [sequence, []]
    return unique_map


import os

def check_sequences_in_group_files(sequences_to_check, duplicate_values):
    result = []
    for tup in duplicate_values:
        seq = tup[0]
        if seq in sequences_to_check:
            result.append(tup)
    return result






