
import Algorithm2
import Decimation
import Generate_sequence
import os
import json
import time
import numpy as np
import pandas as pd
from datetime import datetime
from multiprocessing import Pool, cpu_count, Manager, Lock
import galois

# ✅ Define parameters
m = 8  # Field order
num_pieces = 1 # Number of pieces to divide the range into
start_index = 1  # Start index of combinations to process (1-based)
end_index = 1 # End index of combinations to process (1-based)
num_cores = cpu_count()  # Number of CPU cores to use

# ✅ Create a folder named with the value of m
folder_name = str(m)
os.makedirs(folder_name, exist_ok=True)

# ✅ Get MATLAB-compatible primitive polynomial
primitive_poly = galois.matlab_primitive_poly(2, m)
GF = galois.GF(2 ** m, irreducible_poly=primitive_poly, repr="power")

if 25 <= m <= 63:
    gf_compiled = GF.compile("jit-calculate")
elif m < 25:
    gf_compiled = GF.compile("jit-lookup")
    gf_table = {int(alpha): i for i, alpha in enumerate(GF.elements)}
else:
    gf_compiled = GF.compile("python-calculate")

# ✅ Function to compute autocorrelation using sequence differences
def compute_difference(sequence):
    N = len(sequence)
    results = []
    for k in range(N):
        shifted_sequence = np.roll(sequence, k)
        agreements = np.sum(sequence == shifted_sequence)
        disagreements = N - agreements
        result = agreements - disagreements
        results.append(result)
    return results

# ✅ Compute balance of a sequence
def calculate_balance(sequence):
    d = np.sum(sequence)
    return len(sequence) - 2 * d

# ✅ Function to get power representation safely
def get_power_representation(value):
    if value == 0:
        return None
    field_element = GF(value)
    try:
        return int(field_element.log())
    except AttributeError:
        return None

# ✅ Function to create pieces based on number of pieces
def create_pieces(num_pieces):
    total_elements = 2 ** m - 1
    elements_per_piece = total_elements // num_pieces
    pieces = []
    for i in range(num_pieces):
        start = i * elements_per_piece + 1
        end = (i + 1) * elements_per_piece if i != num_pieces - 1 else total_elements
        pieces.append((start, end))
    with open(f"{folder_name}/pieces.txt", "w") as f:
        for i, (start, end) in enumerate(pieces, 1):
            f.write(f"Piece {i}: From {start} to {end}\n")
    return pieces

# ✅ Function to generate all combinations and save to file
def generate_all_combinations(num_pieces):
    combinations = []
    with open("all_piece_combinations.txt", "w") as f:
        for x0_piece in range(1, num_pieces + 1):
            for mu_piece in range(1, num_pieces + 1):
                combinations.append((x0_piece, mu_piece))
                f.write(f"x0_piece={x0_piece}, mu_piece={mu_piece}\n")
    return combinations

# ✅ Function to load selected combinations from range
def load_selected_combinations_from_range(start_idx, end_idx, file_path="all_piece_combinations.txt"):
    combos = []
    with open(file_path, "r") as f:
        all_lines = f.readlines()
        selected_lines = all_lines[start_idx - 1:end_idx]
        for line in selected_lines:
            if "x0_piece=" in line and "mu_piece=" in line:
                parts = line.strip().split(",")
                x0 = int(parts[0].split("=")[1])
                mu = int(parts[1].split("=")[1])
                combos.append((x0, mu))
    print(f"🔢 Loaded combos #{start_idx} to #{end_idx} ({len(combos)} total)")
    return combos


# ✅ Function to process a single combination
def process_combination(params):
    power_x0, power_mu = params
    # lock = Lock()
    # start_time = time.perf_counter()

    alpha = GF.primitive_element
    Xn = alpha ** power_x0
    R = alpha ** power_mu
    one_ele = alpha ** (2 ** m - 1)

    sequence = []
    unique_powers = set()

    while True:
        int_value = int(Xn)
        if m < 25:
            power_repr = gf_table.get(int_value, -1)
        else:
            power_repr = get_power_representation(int_value) or -1

        if power_repr in unique_powers:
            break

        sequence.append(int_value)
        unique_powers.add(power_repr)
        Xn = Xn * R * (Xn + one_ele)

    binary_sequence = [int(x) % 2 for x in sequence]

    balance = calculate_balance(binary_sequence)
    unique_vals = compute_difference(binary_sequence)
    unique_vals = [abs(val) for val in unique_vals]
    acr_max = max(set(unique_vals[1:])) if len(unique_vals) > 1 else 0
    # execution_time = time.perf_counter() - start_time

    result = {
        "power_x0": int(power_x0),
        "power_mu": int(power_mu),
        "period": int(len(binary_sequence)),
        "acr_max": int(acr_max),
        "balance": int(balance)
    }

    return binary_sequence,result


if __name__ == "__main__":
    # start_timestamp = datetime.now()

    # Read all the data from 'm8_unique_period_28.txt'

    input_file = "m8_unique_period_28.txt"
    input_acr_value = 4
    input_balance_value = 2
    result = Generate_sequence.generate_sequence_v2(input_file,input_acr_value,input_balance_value)
    all_sequence = []
    for item in result:
        power_x0 = int(item[0])
        power_mu = int(item[1])
        period = int(item[2])
        acr_val = item[3]
        balance_val = item[4]
        params = [power_x0,power_mu]
        binary_sequence,resultVal = process_combination(params)
        sequence = ""
        for ele in binary_sequence:
            sequence += str(ele)
        all_sequence.append(sequence)

    unique_binary_sequence = Algorithm2.find_unique_sequences_v4(all_sequence)

    res = []
    for ele in all_sequence:
        decimation = Decimation.generate_sequences_from_sequence_v3(ele)
        for item in decimation:
            res.append(item)
    # print(len(res))

    uniq_ans = Algorithm2.find_unique_sequences_v4(res)
    print(uniq_ans)
    # print(len(uniq_ans))
    #
    # decimation_of_unique_seq = []
    # for j in uniq_ans:
    #     dec = Decimation.generate_sequences_from_sequence_v3(j)
    #     for k in dec:
    #         decimation_of_unique_seq.append(k)
    #
    # ans = Algorithm2.find_unique_sequences_v4(decimation_of_unique_seq)
    # print(ans)
    # print(len(ans))
    #
    # for seq in unique_binary_sequence:
    #     decimated_sequence_list = Decimation.generate_sequences_from_sequence_v3(seq)
    #     unique_after_decimation = Algorithm2.find_unique_sequences_v4(decimated_sequence_list)
    #     print(unique_after_decimation)
    #     print(len(unique_after_decimation))
    # # print(all_sequence,len(all_sequence))
    # print(unique_binary_sequence,len(unique_binary_sequence))








