
pub fn id_matrix(n : usize) -> Vec<Vec<f64>> {
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
    
pub fn inverse(matrix : &Vec<Vec<f64>>) -> Option<Vec<Vec<f64>>> {
    let n = matrix.len();
    let mut inv = id_matrix(n);
    let mut matrix = matrix.clone();
    let eps : f64 = 1e-12;
        
    for i in 0..n{
        let mut swap = i;
        for r in i..n {
            if matrix[r][i].abs() > matrix[swap][i].abs() {
                swap = r;
            }
        }
        matrix.swap(i, swap);
        inv.swap(i, swap);

        let pivot = matrix[i][i];
            
        if pivot.abs() < eps {
            return None;
        }

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