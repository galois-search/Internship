# read data from file and generate a binary sequence for that
# Given data in file: {"power_x0": 15, "power_mu": 13, "period": 12, "acr_max": 12, "balance": 0}

def generate_sequence(Input_file):
    with open(Input_file,"r") as infile:
        result = []
        for line in infile:
            parts = line.split(", ")
            power_x0 = parts[0].split(": ")[1]
            power_mu = parts[1].split(": ")[1]
            length = parts[2].split(": ")[1]
            result.append([power_x0,power_mu,length])

        return result


def generate_sequence_v2(Input_file,acr,balance):
    with open(Input_file,"r") as infile:
        result = []
        for line in infile:
            parts = line.split(", ")
            power_x0 = parts[0].split(": ")[1]
            power_mu = parts[1].split(": ")[1]
            length = parts[2].split(": ")[1]
            acr_value = int(parts[3].split(": ")[1])
            balance_value = int(parts[4].split(": ")[1].rstrip("}\n"))

            if abs(acr_value) <= acr and abs(balance_value) <= balance:
                result.append([power_x0,power_mu,length,acr_value,balance_value])

        return result
