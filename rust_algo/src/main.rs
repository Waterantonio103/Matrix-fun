fn main() {
    println!("Hello, world!");

    data_type();

    testing(5);

    human("James", 18, 179.3, 80.7);

    println!("The global const value is : {}", GLOBAL);

    let total : f32 = {
        let price : f32 = 200.0;
        let qty : u32 = 5;
        price * qty as f32
    };
    println!("Total = {:?}", total);

    let a : i32 = 17;
    let b : i32 = 3;
    let result = mult(a,b);
    println!("Multiplication of {} by {} = {}",a,b, result);

    let _bmi : f64 = bmi(80.7,179.3);
    println!("My BMI is : {:.4}", _bmi);
}

const GLOBAL : i32 = {
    2
};

fn data_type(){
    let array : [i32;3] = [1,2,3];
    println!("Array : {:?}", array);

    let tuple : (&str, i32) = ("James", 18);
    println!("Tuple : {:?}", tuple);

    let slice_array= &array;
    println!("Slice : {:?}", slice_array);

    let mut stringy : String = String::from("Hello, World");
    println!("String before mut : {}", stringy);
    stringy.push_str(", How are you?");
    println!("String after mut : {}", stringy);

    let string_slice : String = String::from("Yo, whats going on");
    let slice : &str = &string_slice[0..9];
    println!("String to be sliced : {}", string_slice);
    println!("Slice of string : {}", slice);
}

fn testing(x : i32){
    println!("Your number is {}", x);
}

fn human(name : &str, age : u32, height : f32, weight : f32){
    println!("Hi, my name is {}, I am {} years old, I am {} cm tall and weigh roughly {} kg.",name, age, height, weight)
}

fn mult(a : i32, b : i32) -> i32{
    a * b
}

fn bmi(weight : f64, height : f64) -> f64 {
    weight / height.powi(2)
}
