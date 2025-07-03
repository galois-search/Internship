import Acr_Bal_Program
import Algorithm2
import Decimation
import Decimation_V02
import Generate_sequence
import os
import json
import time
import numpy as np
import pandas as pd
from datetime import datetime
from multiprocessing import Pool, cpu_count, Manager, Lock
import galois

import filter_input_data
import unique_sequence

# ✅ Define parameters
m = 9  # Field order
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

    input_file = "m9_unique_period_127.txt"
    input_acr_value = 2
    input_balance_value = 2
    result = filter_input_data.filter_data(input_file,input_acr_value,input_balance_value)
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
        all_sequence.append([sequence,params])

    print(len(all_sequence))

    unique_sequence_before_decimation = unique_sequence.find_unique_sequences_v5(all_sequence)

    print(len(unique_sequence_before_decimation))

    decimation_of_unique_sequence = []

    for element in unique_sequence_before_decimation:
        ele = element[0]
        decimated_values = Decimation_V02.generate_decimated_sequences(ele)
        for val in decimated_values:
            decimation_of_unique_sequence.append([val,element[1]])

    print(len(decimation_of_unique_sequence))

    unique_sequence_after_decimation = unique_sequence.find_unique_sequences_v5(decimation_of_unique_sequence)

    print(len(unique_sequence_after_decimation))

    file_name = input_file.removesuffix('.txt')

    with open(f"{file_name}_unique_before_decimation.txt",'w') as of:
        for value in unique_sequence_before_decimation:
            original_seq = value[0]
            seq = [int(d) for d in str(original_seq)]
            acr = Acr_Bal_Program.compute_acr(seq)
            balance = Acr_Bal_Program.calculate_balance(seq)
            of.write(f"power_x0 : {value[1][0]},power_mu : {value[1][1]},period : {len(original_seq)},acr_val : {acr},balance : {balance},sequence : {original_seq}\n")

    with open(f"{file_name}_unique_sequence.txt",'w') as output_file:
        for value in unique_sequence_after_decimation:
            original_seq = value[0]
            seq = [int(d) for d in str(original_seq)]
            acr = Acr_Bal_Program.compute_acr(seq)
            balance = Acr_Bal_Program.calculate_balance(seq)
            output_file.write(f"power_x0 : {value[1][0]},power_mu : {value[1][1]},period : {len(original_seq)},acr_val : {acr},balance : {balance},sequence : {original_seq}\n")

