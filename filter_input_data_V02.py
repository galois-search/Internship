def filter_data(Input_file,acr,balance):
    with open(Input_file,"r") as infile:
        result = []
        for line in infile:
            parts = line.split(", ")
            power_x0 = parts[0].split(": ")[1]
            power_mu = parts[1].split(": ")[1]
            length = parts[2].split(": ")[1]
            acr_value = int(parts[3].split(": ")[1])
            balance_value = int(parts[4].split(": ")[1].rstrip("}\n"))

            if abs(acr_value) <= abs(acr) and abs(balance_value) <= abs(balance):
                result.append([power_x0,power_mu,length,acr_value,balance_value])

        return result