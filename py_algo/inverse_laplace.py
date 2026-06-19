def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        det = 0
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += ((-1) ** i) * matrix[0][i] * determinant(submatrix)
        return det
    
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

def estimate_calc_time(base_size, base_seconds, target_size):
    estimate = base_seconds
    if target_size > base_size:
        for size in range(base_size + 1, target_size + 1):
            estimate *= size
    elif target_size < base_size:
        for size in range(base_size, target_size, -1):
            estimate /= size
    return estimate
