fn main(){
    let s1 = String::from("Hello, World!");
    let s2 = s1;
    let len = calc_len(&s2);
    println!("The len of '{}' is : {}\n",s2,len);

    println!("------------------------------------------------------------------\n");

    let mut _x : i32 = 10;
    let _y: &mut i32 = &mut _x;
    let inc : i32 = 3;
    let dec : i32 = 8;
    *_y += inc;
    *_y -= dec;
    println!("y equals : {}, it was increased by {} then decreased by {}\n",_y, inc, dec);

    println!("------------------------------------------------------------------\n");

    let mut account = Bank{
        owner : String::from("James"),
        balance : 1246.09,
    };
    account.withdraw(723.28);
    account.deposit(723.28);

    println!("-------------------------------------------------------------------\n");

    let mut doggy_array =  
    [
    Dog{
        breed : String::from("German Shepherd"),
        name : String::from("Jimbo"),
        age : 3,
        weight : 25.3,
        price : 455.00,
        alive : true,
    },
    Dog{
        breed : String::from("Golden Retriever"),
        name : String::from("Jameson"),
        age : 7,
        weight : 22.3,
        price : 235.00,
        alive : true,
    },
    Dog{
        breed : String::from("Chihuaha"),
        name : String::from("Jim"),
        age : 1,
        weight : 5.3,
        price : 35.00,
        alive : true,
    },
    Dog{
        breed : String::from("Doberman"),
        name : String::from("James III"),
        age : 5,
        weight : 26.6,
        price : 1235.00,
        alive : true,
    },
    ];

    for i in 0..doggy_array.len(){
        doggy_array[i].dog_info();
    }
    
    doggy_array[2].rename(String::from("Jameis"));
    doggy_array[1].rename(String::from("Jimerson"));
    doggy_array[3].rename(String::from("JimmyJoe"));

    let wait_time = 12;

    for i in 0..doggy_array.len(){
        doggy_array[i].wait(wait_time);
    }
    
    println!("Modifications below ->\n");

    for j in 0..doggy_array.len(){
        doggy_array[j].dog_info();
    }

    let mut message = format!("You waited {} years\n",wait_time);

    if doggy_array.iter().any(|doggy|doggy.alive == false){
        for doggy in doggy_array.iter().filter(|doggy|doggy.alive == false){
            message.push_str(&format!(" {} died :(\n", doggy.name));
        }
    } else {
        message.push_str(" No dogs died :)\n");
    }

    println!("{}", message);

}

fn calc_len(s : &String) -> usize{
    s.len()
}

struct Bank {
    owner : String,
    balance : f64,
}

impl Bank {
    fn withdraw(&mut self, amount : f64){
        println!("You are withdrawing {:.2} from account with owner '{}'\n", amount, self.owner);
        self.balance -= amount;
        self.check_balance();
    }

    fn deposit(&mut self, amount : f64){
        println!("You are depositing {:.2} to account with owner {}\n", amount, self.owner);
        self.balance += amount;
        self.check_balance();
    }

    fn check_balance(&self){
        println!("Current balance for account owner '{}' is : {:.2}\n", self.owner, self.balance);
    }
}

struct Dog {
    breed : String,
    name : String,
    age : u16,
    weight : f32,
    price : f32,
    alive : bool,
}

impl Dog {
    fn dog_info(&self){
        if self.alive == false{
            println!("Unfortunately, {} is dead :( at age {}\n",self.name, self.age);
        } else if self.age == 15{
            println!("Doggy {} is now {} years old, the chap is ready to go, say goodbye\n",self.name,self.age);
        } else {
            println!("This dog's name is {}, he is a {}, he is {} years old, weighs roughly {} kg and costs ${}\n",self.name,self.breed,self.age,self.weight,self.price);
        }
    }


    fn rename(&mut self, new_name : String){
        self.name = new_name;
    }

    fn wait(&mut self, time : u16){
        self.age += time;
        if self.age > 15{
            self.alive = false;
        }
    }
}