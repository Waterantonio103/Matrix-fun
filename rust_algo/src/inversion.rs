pub fn invert(matrix: &Vec<Vec<f64>>, value : f64) -> Vec<Vec<f64>> {
    let mut out: Vec<Vec<f64>> = Vec::new();

    for row in matrix.iter() {
        let mut out_row: Vec<f64> = Vec::new();

        for pixel in row.iter() {
            let inv_pix = (value - *pixel).clamp(0.0, 255.0);
            out_row.push(inv_pix);
        }

        out.push(out_row);
    }

    out
}