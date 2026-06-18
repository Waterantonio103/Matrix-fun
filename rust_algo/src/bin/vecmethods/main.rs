use std::time::Instant;

fn main() {
    let matrix : Vec<Vec<f64>> = vec![
        vec![2.0, 1.0, 0.0, 3.0, 4.0, 1.0, 2.0, 0.0, 1.0, 5.0],
        vec![0.0, 3.0, 1.0, 2.0, 0.0, 4.0, 1.0, 2.0, 3.0, 1.0],
        vec![1.0, 0.0, 4.0, 1.0, 2.0, 0.0, 3.0, 1.0, 2.0, 4.0],
        vec![3.0, 2.0, 1.0, 5.0, 1.0, 2.0, 0.0, 4.0, 1.0, 3.0],
        vec![4.0, 1.0, 2.0, 0.0, 6.0, 1.0, 2.0, 3.0, 0.0, 1.0],
        vec![1.0, 4.0, 0.0, 2.0, 1.0, 7.0, 3.0, 0.0, 2.0, 1.0],
        vec![2.0, 1.0, 3.0, 0.0, 2.0, 3.0, 8.0, 1.0, 4.0, 0.0],
        vec![0.0, 2.0, 1.0, 4.0, 3.0, 0.0, 1.0, 9.0, 2.0, 3.0],
        vec![1.0, 3.0, 2.0, 1.0, 0.0, 2.0, 4.0, 2.0, 10.0, 1.0],
        vec![5.0, 1.0, 4.0, 3.0, 1.0, 1.0, 0.0, 3.0, 1.0, 11.0],
    ];

    let start = Instant::now();

    let det = determinant(&matrix);
    println!("Determinant of {:?} = {det}", matrix);

    match reduc_identity(&matrix) {
        Some(inv) => println!("Inverse: {:?}", inv),
        None => println!("Matrix is not invertible"),
    }
    let elapsed = start.elapsed();

    println!("Total time : {:.6}s", elapsed.as_secs_f64());

}

fn determinant(matrix : &Vec<Vec<f64>>) -> f64 {
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

fn row_echelon(matrix : &Vec<Vec<f64>>) -> (Vec<Vec<f64>>, u32) {
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

fn id_matrix(n : usize) -> Vec<Vec<f64>> {
    let mut id : Vec<Vec<f64>> = Vec::new();
    
    for _i in 0..n{
        id.push(vec![0.0;n]);
    };

    let l = id.len();

    for i in 0..l{
        id[i][i] += 1.0;
    };

    id
}

fn reduc_identity(matrix : &Vec<Vec<f64>>) -> Option<Vec<Vec<f64>>> {
    let n = matrix.len();
    let mut inv = id_matrix(n);
    let mut matrix = matrix.clone();

    if determinant(&matrix) == 0.0 {
        return None
    }

    for i in 0..n{
        let pivot = matrix[i][i];

        if pivot != 1.0{
            for b in 0..n{
                matrix[i][b] /= pivot;
                inv[i][b] /= pivot;
            }
        }
        for j in 0..n{
            if j == i {
                continue;
            }

            let fac = matrix[j][i];

            for k in 0..n{
                matrix[j][k] -= fac * matrix[i][k];
                inv[j][k] -= fac * inv[i][k];
            }
            
        }
    }
    Some(inv)
}