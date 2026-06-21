# Image Matrix Inversion Experiment

A small experimental project that takes an image as input, extracts its RGB values into separate **R**, **G**, and **B** matrices, computes matrix inverses, and rebuilds the image from the transformed pixel values.

The goal is experimentation, not image quality.

## Current Status

Inverse algorithms have been written in **Python** and **Rust**.  
Image modification code has been written in **Rust** using the **Image** crate.

## Methods

| Algorithm | Complexity |
|---|---:|
| Laplace / Cofactor Expansion | O(n!) |
| Gaussian Row Elimination | O(n³) |
| Gauss-Jordan Elimination | O(n³) |

## Results

<table>
  <tr>
    <td align="center">
      <img src="assets/starry_night.jpg" alt="Van Gogh's Starry Night" width = "300">
      <br>
      <b>Original</b> 
      <br>
      <sub><i>(Van Gogh's Starry Night)</i></sub>
    </td>
    <td align="center" width="80">
      <h1>→</h1>
    </td>
    <td align="center" width="300">
      <img src="assets/not_so_starry_night.png">
      <br>
      <b>After Matrix Inversion</b>
      <br>
      <sub><i>(Waterantonio103's Not So Starry Night)</i></sub>
    </td>
  </tr>
</table>

# Other Modifications Tested

## Inverting the pixels

<img src="assets/inverted_starry_night.png" width="400">

## Clamping RGB Channel Values by a fixed amount per channel

<img src="assets/hellish_night.png" width="400">

<table>
  <tr>
    <td align="center">
      <img src="assets/fairs.jpg"  width = "300">
      <br>
      <b>Original</b> 
      <br>
      <sub><i>(#fairs 👌)</i></sub>
    </td>
    <td align="center" width="80">
      <h1>→</h1>
    </td>
    <td align="center" width="300">
      <img src="assets/invertfairs.png">
      <br>
      <b>After Inverting</b>
      <br>
      <sub><i>(👌👌👌)</i></sub>
    </td>
  </tr>
</table>

<img src="assets/hellfairs.png">


