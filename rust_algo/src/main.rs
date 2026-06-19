mod inverse;
mod determinant;
mod vecgen;

use inverse::*;
use determinant::*;
use vecgen::rand_vec;

use std::time::Instant;

fn main(){
    let matrix = 
    match rand_vec(500, 0.0, 255.0) {
        Some(m) => m,
        None => {
            println!("Invalid range");
            return;
        }
    };

    match inverse(&matrix) {
        Some(inv) => {
            println!("Inverse: {:?}", inv);
        }
        None => {
            println!("Matrix non-invertible");
        }
    };

    let start = Instant::now();
    let det = determinant(&matrix);
    let elapsed = start.elapsed();
    println!("Determinant = {det}\nTime : {}s", elapsed.as_secs_f64());
    println!("------------------------------------------------------");
    
    let start = Instant::now();
    match inverse(&matrix){
        Some(inv) => {
            let elapsed = start.elapsed();
            println!("Inverse : {:?}\nTime : {}s", inv, elapsed.as_secs_f64());
        }
        None => {
            println!("Matrix non-invertible");
        }
    }

}