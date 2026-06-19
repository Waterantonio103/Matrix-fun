def row_echelon(matrix):
    n = len(matrix)
    matrix = [row[:] for row in matrix]
    swap = 0
    for i in range(n - 1):
        if matrix[i][i] == 0:
            for r in range(i + 1, n):
                if matrix[r][i] != 0:
                    matrix[i], matrix[r] = matrix[r], matrix[i]
                    swap += 1
                    break
                else:
                    return matrix, swap  
            
        pivot = matrix[i]

        for j in range(i + 1, n):
            f = -matrix[j][i] / matrix[i][i]

            matrix[j] = [
                x + y * f
                for x, y in zip(matrix[j], pivot)
            ]

    return matrix, swap

def determinant(matrix):
    matrix, swap = row_echelon(matrix)
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        det = 1
        for i in range(n):
            det *= matrix[i][i]

        det *= ((-1)**(swap))
        return det

    return matrix

def cofactor(matrix):
    n = len(matrix)
    cof = []
    for i in range(n):
        cofactor_row = []
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
            det = determinant(submatrix)
            if (i + j) % 2 != 0:
                det = det*(-1)
                cofactor_row.append(det)
            else:
                cofactor_row.append(det)
        cof.append(cofactor_row)
    return cof

def adjugate(matrix, cof):
    n = len(matrix)
    adj = [row[:] for row in cof]
    for i in range(n):
        for j in range(i+1, n):
            adj[i][j] , adj[j][i] = adj[j][i] , adj[i][j]
    return adj

def inverse(matrix,det,adj):
    n = len(matrix)
    if det == 0:
        return "No inverse exists (determinant is 0)"

    inv = []
    for i in range(n):
        inverse_row = []
        for j in range(n):
            inverse_row.append(adj[i][j] / det)
        inv.append(inverse_row)
    return inv
