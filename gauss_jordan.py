from inverse_gauss import determinant

def identity(matrix):
    n = len(matrix)
    
    ide = [[0 for j in range(n)] for i in range(n)]

    for i in range(n):
        ide[i][i] = 1

    return ide

def reduc_identity(matrix):
    n = len(matrix)
    inv=identity(matrix)
    if determinant(matrix) == 0:
        return None
    for i in range(n):
        pivot = matrix[i][i]
        
        if pivot != 1:
            matrix[i] = [x/pivot for x in matrix[i]]
            inv[i] = [x/pivot for x in inv[i]]
            
        for j in range(n):
                
            if j==i:
                continue

            fac = matrix[j][i]
            matrix[j] = [matrix[j][k] - fac*matrix[i][k] for k in range(len(matrix[j]))]
            inv[j] = [inv[j][k] - fac*inv[i][k] for k in range(len(inv[j]))]


    return inv
            
