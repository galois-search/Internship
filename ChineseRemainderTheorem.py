"""
given three sequences operations to perform on them
matrix = [['a','h','o'],
          ['b','i','p'],
          ['c','j','q'],
          ['d','k','r'],
          ['e','l','s'],
          ['f','m','t'],
          ['g','n','u']]

Desired output : {a,i,q,d,l,t,g,h,p,c,k,s,f,n,o,b,j,r,e,m,u}
"""

def solution(list_of_sequence):

    matrix = [[s[i] for s in list_of_sequence] for i in range(len(s1))]
    print(matrix)

    rows = len(matrix)
    cols = len(matrix[0])

    result = []

    for offset in range(cols):
        for i in range(rows):
            col = (i + offset) % cols
            row = i
            if row < rows and col < cols:
                result.append(matrix[row][col])

    return result

'''
s1 = 'r7H8F2kQvJ'
s2 = '3qZ5m1VwAX'
s3 = 'nW0yGz6fUe'
s4 = 'u2Kp4Yj9tN'
s5 = 'xB1hT8L5vS'
'''

s1 = 'abcdefg'
s2 = 'hijklmn'
s3 = 'opqrstu'
s4 = 'vwxyz12'

strings = [s1,s2,s3,s4]
print(''.join(solution(strings)))
