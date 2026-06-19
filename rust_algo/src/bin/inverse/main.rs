use std::time::Instant;
use rand::random_range;

fn main() {
        let vec_size : i32 = 500;
        let matrix: Vec<Vec<f64>> = rand_vec(vec_size);
        
        let start1 = Instant::now();
        match reduc_identity(&matrix) {
            Some(_inv) => println!("✅"), 
            None => println!("Matrix is not invertible"),
        }
        let elapsed1 = start1.elapsed();
        println!("Matrix size : {vec_size}");
        println!("Inverse time : {:.6}s", elapsed1.as_secs_f64());
    }
    
    fn rand_vec(size : i32) -> Vec<Vec<f64>> {
        let mut matrix : Vec<Vec<f64>> = Vec::new();
        
        for _i in 0..size{
            let mut inner : Vec<f64> = Vec::new();
            
            for _j in 0..size{
                let n : f64 = random_range(0.0..255.0);
                inner.push(n);
            }
            matrix.push(inner)
        };
        
        matrix
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