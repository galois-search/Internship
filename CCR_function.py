from itertools import combinations

import numpy as np

def compute_cross_correlation(seq1, seq2):
    seq1 = np.array(seq1)
    seq2 = np.array(seq2)
    N = len(seq1)
    results = []
    for k in range(N):
        shifted_seq2 = np.roll(seq2, k)
        agreements = np.sum(seq1 == shifted_seq2)
        disagreements = N - agreements
        result = agreements - disagreements
        results.append(int(result))
    return results


def compute_ccr(list_of_binary_sequence):
    ccr_results = {}
    for seq1, seq2 in combinations(list_of_binary_sequence, 2):
        seq1_str = ''.join(str(x) for x in seq1)
        seq2_str = ''.join(str(x) for x in seq2)
        cc = compute_cross_correlation(seq1, seq2)
        ccr_max = max(abs(val) for val in cc)
        ccr_results[(seq1_str, seq2_str)] = ccr_max
    max_pair = max(ccr_results, key=ccr_results.get)
    print(ccr_results)
    return max_pair,ccr_results[max_pair],ccr_results


def read_sequences_from_file(input_file):
    with open(input_file,'r') as file:
        list_of_sequence = []
        for line in file:
            parts = line.strip().split(",")
            sequence = parts[5].split(" : ")[1]
            seq_arr = [int(d) for d in str(sequence)]
            list_of_sequence.append(seq_arr)
    return list_of_sequence

if __name__ == "__main__":
    file_name = "m10_UniqueBeforeDecimation/m10_unique_period_255_unique_1_-1.txt"
    listOfSeq = read_sequences_from_file(file_name)
    max_pair, ccr_max, ccr_results = compute_ccr(listOfSeq)
    print("Most correlated pair:")
    print(max_pair[0])
    print(max_pair[1])
    print("Maximum CCR:", ccr_max)

    # Write CCR results to file
    output_ccr_file = f"{file_name.split('/')[1].removesuffix('.txt')}_ccr_results.txt"
    with open(output_ccr_file, 'w') as f:
        for (seq1_str, seq2_str), ccr_val in ccr_results.items():
            f.write(f"Seq1: {seq1_str}, Seq2: {seq2_str}, CCR: {ccr_val}\n")
    print(f"CCR results written to {output_ccr_file}")
