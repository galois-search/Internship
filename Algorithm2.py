# Program to find unique shift sequences
import os

from numba.cpython.listobj import list_is


def find_unique_sequences():
    with open("generate_test.txt", "r") as infile, open("UniqueSequencenew.txt", "a") as outfile:
        for line in infile:
            ListOfSequence = line.strip().split(" ")

            uniqueSequence = {}
            for sequence in ListOfSequence:
                currentSequence = sequence
                shifted_sequence = ""
                while shifted_sequence != sequence:
                    shifted_sequence = currentSequence[1:] + currentSequence[0]
                    if shifted_sequence in uniqueSequence:
                        uniqueSequence[shifted_sequence] += 1
                        currentSequence = shifted_sequence
                    else:
                        uniqueSequence[shifted_sequence] = 1
                        currentSequence = shifted_sequence

            outfile.write(f"{ListOfSequence[0]} : ")
            for key, value in uniqueSequence.items():
                if key in ListOfSequence and value == 1:
                    outfile.write(f"{key} ")
            outfile.write("\n")


# find_unique_sequences()

def find_unique_sequences_v2(ListOfSequence):
    uniqueSequence = []
    for sequence in ListOfSequence:
        currentSequence = sequence
        shifted_sequence = ""
        while shifted_sequence != sequence:
            shifted_sequence = currentSequence[1:] + currentSequence[0]
            if shifted_sequence in uniqueSequence:
                break
            else:
                uniqueSequence.append(shifted_sequence)
                currentSequence = shifted_sequence

    # for ele in uniqueSequence:
    #     if ele in ListOfSequence:
    #         print(ele)

    # folder = f"{folder_name}_"
    # os.makedirs(folder, exist_ok= True)
    # fileName = f"{params[0]}_{params[1]}_{period}.txt"
    # filePath = os.path.join(folder,fileName)
    # with open(filePath, "a") as file:
    #     for key, value in uniqueSequence.items():
    #         if key in ListOfSequence and value == 1:
    #             file.write(f"{key} \n")


def find_unique_sequences_v3(ListOfSequence,params,period,acr,balance,folder_name):
    unique_sequence = []
    for sequence in ListOfSequence:
        if sequence in unique_sequence:
            continue
        else:
            current_sequence = sequence
            shifted_sequence = ""
            while shifted_sequence != sequence:
                shifted_sequence = current_sequence[1:] + current_sequence[0]
                if shifted_sequence in unique_sequence:
                    break
                else:
                    current_sequence = shifted_sequence

            if shifted_sequence == sequence and sequence not in unique_sequence:
                unique_sequence.append(sequence)

    folder = folder_name.removesuffix(".txt")
    os.makedirs(folder, exist_ok= True)
    fileName = f"{params[0]}_{params[1]}_{period}.txt"
    filePath = os.path.join(folder,fileName)
    with open(filePath, "w") as file,open(f"{folder}_unique_count.txt","a") as count_file:
        for element in unique_sequence:
            file.write(f"{element} : S{ListOfSequence.index(element) + 1}\n")
        count_file.write(f"[power_x0: {params[0]}, power_mu: {params[1]}, period: {period}, acr_value: {acr}, balance: {balance}, unique_sequence_count: {len(unique_sequence)}]\n")



def find_unique_sequences_v4(ListOfSequence):
    unique_sequence = []
    for sequence in ListOfSequence:
        if sequence in unique_sequence:
            continue
        else:
            current_sequence = sequence
            shifted_sequence = ""
            while shifted_sequence != sequence:
                shifted_sequence = current_sequence[1:] + current_sequence[0]
                if shifted_sequence in unique_sequence:
                    break
                else:
                    current_sequence = shifted_sequence

            if shifted_sequence == sequence and sequence not in unique_sequence:
                unique_sequence.append(sequence)

    return unique_sequence


