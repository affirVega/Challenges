use std::io::{self, Read, Write};

fn main() {
    let mut buf = String::new();
    let rot = 13u8;
    let stdin = io::stdin();

    {
        let mut handle = stdin.lock();
        match handle.read_to_string(&mut buf) {
            Ok(_) => (),
            Err(e) => panic!("Error while reading stdin: {}", e)
        }
    }

    let mut outstr = String::new();
    for (i, symbol) in buf.char_indices() {
        if symbol >= 'a' && symbol <= 'z' {
            outstr.push(((symbol as u8 - 'a' as u8 + rot) % 23 + 'a' as u8) as char);
            continue;
        }
        else if symbol >= 'A' && symbol <= 'Z' {
            outstr.push(((symbol as u8 - 'A' as u8 + rot) % 23 + 'A' as u8) as char);
            continue;
        }
        outstr.push(symbol);
    }

    print!("{}", outstr);
}
