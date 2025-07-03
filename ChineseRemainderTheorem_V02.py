def solution(list_of_sequence):

    matrix = [[s[i] for s in list_of_sequence] for i in range(len(s1))]
    print(matrix)

    rows = len(matrix)
    cols = len(matrix[0])

    result = []

    i,j =0,0
    count = 0
    while count < rows * cols:

        if i < rows and j < cols:
            result.append(matrix[i][j])
            i = i + 1
            j = j + 1
            count += 1

        elif i < rows and j >= cols:
            j = 0
        elif i >= rows and j < cols:
            i = 0
        elif i >= rows and j >= cols:
            break

    return result



s1 = 'abcdefg'
s2 = 'hijklmn'
s3 = 'opqrstu'
s4 = 'vwxyz12'
s5 = '3456789'

strings = [s1,s2,s3,s4,s5]
print(''.join(solution(strings)))
