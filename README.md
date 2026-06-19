The goal of this small fun project repo is to take an image as input, extract its rgb values into individual R G and B matrices, calculate their inverses (plus a little scaling and fooling around) and re-build the image from the new pixel values (will likely produce a visual mess nowhere close to the initial image -- just for fun and experimenting). 
The current preferred method of choice is Gauss Jordan. 
Current status : inverse algorithms written in python and in rust (Laplace-Cofactor ~O(n!), Gauss Row elemination ~O(n^3), Gauss-Jordan ~O(n^3)).
