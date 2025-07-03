# Program for decimation

def generate_sequences_from_sequence():
    with open("RandomSequence.txt", "r") as infile, open("generate_test.txt", "a") as outfile:
        for OriginalSequence in infile:
            OriginalSequence = OriginalSequence.rstrip()
            n = len(OriginalSequence)
            result = []
            for i in range(1, n):
                sequence = ""
                index = 0
                while len(sequence) < n:
                    sequence = sequence + OriginalSequence[index]
                    index = (index + i) % n
                result.append(sequence)

            for item in result:
                outfile.write(item + " ")
            outfile.write("\n")


def generate_sequences_from_sequence_v2(binary_sequence):
    sequence = ""
    for ele in binary_sequence:
        sequence += str(ele)
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

def generate_sequences_from_sequence_v3(sequence):

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

