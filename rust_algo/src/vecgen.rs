use rand::random_range;

pub fn rand_vec(size : i32, range_lower : f64, range_upper : f64) -> Option<Vec<Vec<f64>>> {
        if range_lower > range_upper {
            return None;
        }
        
        let mut matrix : Vec<Vec<f64>> = Vec::new();
        
        for _i in 0..size{
            let mut inner : Vec<f64> = Vec::new();
            
            for _j in 0..size{
                let n : f64 = random_range(range_lower..range_upper);
                inner.push(n);
            }
            matrix.push(inner)
        };
        
        Some(matrix)
    }
    