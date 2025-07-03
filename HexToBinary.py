def HexToBinaryConverter(Hex_value):
    BinaryValue = bin(int(Hex_value,16))
    return BinaryValue

HexaValue = "EC757781362D6F9"
print(HexToBinaryConverter(HexaValue))