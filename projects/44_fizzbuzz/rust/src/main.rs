enum FizzBuzz {
    Dividable(&'static str),
    Unmatched(i32)
}

struct StringToNum {
    string: &'static str,
    num: i32
}

fn get_enum(num: i32) -> FizzBuzz {
    let table: [StringToNum; 2] = [
        StringToNum{string: "Fizz", num:3},
        StringToNum{string: "Buzz", num:5},
    ];

    for elem in table {
        if num % elem.num == 0 {
            return FizzBuzz::Dividable(elem.string)
        }
    }

    return FizzBuzz::Unmatched(num);
}

fn main() {
    for i in 1i32..=100i32 {
        match get_enum(i) {
            FizzBuzz::Dividable(text) => println!("{}", text),
            FizzBuzz::Unmatched(_) => println!("{}", i)
        }
    }
}
