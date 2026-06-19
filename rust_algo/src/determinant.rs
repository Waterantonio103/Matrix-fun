pub fn determinant(matrix : &Vec<Vec<f64>>) -> f64 {
    let (matrix, swap) = row_echelon(matrix);
    let n = matrix.len();
        
    if n == 1 {
        return matrix[0][0];
    } else if n == 2 {
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
    } else {
        let mut det = 1.0;
                    
        for i in 0..n{
            det *= matrix[i][i];
        }
        if swap % 2 == 1 {
            det *= -1.0;
        }
        det
    }
}

pub fn row_echelon(matrix : &Vec<Vec<f64>>) -> (Vec<Vec<f64>>, u32) {
    let mut matrix = matrix.clone();
    let n = matrix.len();
    let mut swap: u32 = 0;

    for i in 0..(n-1){
        if matrix[i][i] == 0.0{
            for r in (i+1)..n{
                if matrix[r][i] != 0.0{
                    matrix.swap(i, r);
                    swap += 1;
                    break
                } else {
                    return (matrix, swap);
                }
            }
        }

        let pivot = matrix[i].clone();
                                    
        for j in (i+1)..n{
            let f = -matrix[j][i] / matrix[i][i];
                                        
                for b in 0..matrix[j].len() {
                    matrix[j][b] += pivot[b] * f;
                }
        }
    };

    return (matrix, swap)                        
}

