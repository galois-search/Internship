def generate_decimated_sequences(sequence):
    n = len(sequence)
    result = []
    for i in range(1, n):
        sequence_2 = ""
        index = 0
        while len(sequence_2) < n:
             sequence_2 = sequence_2 + sequence[index]
             index = (index + i) % n
        result.append(sequence_2)
    return result