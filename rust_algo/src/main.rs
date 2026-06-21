mod inverse;
mod determinant;
mod vecgen;
mod inversion;

use inverse::*;
use determinant::*;
use vecgen::rand_vec;
use inversion::invert;

use std::time::Instant;
use image::{DynamicImage, Rgb, RgbImage};

fn main(){

    let input_path = concat!(env!("CARGO_MANIFEST_DIR"), "/../assets/fairs.jpg");
    let output_path = concat!(env!("CARGO_MANIFEST_DIR"), "/../assets/full_output.png");
    let img_dynamic: DynamicImage = image::open(input_path).unwrap();
    let img: RgbImage = img_dynamic.to_rgb8();
    let (width, height): (u32, u32) = img.dimensions();

    let block_size: u32 = width.min(height);

    let mut var = 0;
    let mut out_img: RgbImage = RgbImage::new(width, height);

    let mut rects: Vec<(u32, u32, u32, u32)> = Vec::new();
    rects.push((0, 0, width, height));

    while let Some((start_x, start_y, rect_width, rect_height)) = rects.pop() {
        let sq_size = rect_width.min(rect_height);

        let mut r_vec: Vec<Vec<f64>> = Vec::new();
        let mut g_vec: Vec<Vec<f64>> = Vec::new();
        let mut b_vec: Vec<Vec<f64>> = Vec::new();

        for y in 0..sq_size {
            let mut r_row: Vec<f64> = Vec::new();
            let mut g_row: Vec<f64> = Vec::new();
            let mut b_row: Vec<f64> = Vec::new();

            for x in 0..sq_size {
                let pixel: Rgb<u8> = *img.get_pixel(start_x + x, start_y + y);
                let rgb: [u8; 3] = pixel.0;

                r_row.push(rgb[0] as f64);
                g_row.push(rgb[1] as f64);
                b_row.push(rgb[2] as f64);
            }

            r_vec.push(r_row);
            g_vec.push(g_row);
            b_vec.push(b_row);
        }

        r_vec = invert(&r_vec, 255.0);
        g_vec = invert(&g_vec, 255.0);
        b_vec = invert(&b_vec, 255.0);

        // r_vec = normalize(r_vec, 0.7);
        // g_vec = normalize(g_vec, 0.4);
        // b_vec = normalize(b_vec, 1.2);


        let mut img: RgbImage = RgbImage::new(sq_size, sq_size);

        for y in 0..sq_size {
            for x in 0..sq_size {
                let r = r_vec[y as usize][x as usize].clamp(0.0, 255.0) as u8;
                let g = g_vec[y as usize][x as usize].clamp(0.0, 255.0) as u8;
                let b = b_vec[y as usize][x as usize].clamp(0.0, 255.0) as u8;

                out_img.put_pixel(start_x + x, start_y + y, Rgb([r, g, b]));
            }
        }

        if rect_width > rect_height {
            rects.push((
                start_x + sq_size,
                start_y,
                rect_width - sq_size,
                rect_height,
            ));
        } else if rect_height > rect_width {
            rects.push((
                start_x,
                start_y + sq_size,
                rect_width,
                rect_height - sq_size,
            ));
        }
    }

    out_img.save(output_path).unwrap();
}

fn normalize(mut vec: Vec<Vec<f64>>, contrast: f64) -> Vec<Vec<f64>> {
    let mut sum = 0.0;
    let mut count = 0.0;

    for row in vec.iter() {
        for val in row.iter() {
            sum += val.abs();
            count += 1.0;
        }
    }

    let avg = sum / count;
    let clip = avg * contrast;

    if clip == 0.0 {
        return vec;
    }

    for row in vec.iter_mut() {
        for val in row.iter_mut() {
            *val = val.clamp(-clip, clip);
            *val = ((*val + clip) / (2.0 * clip)) * 255.0;
        }
    }

    vec
}