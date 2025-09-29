use std::env;
use std::io::{self, Read};
use ko_morph::Analyzer;

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    
    let text = if args.is_empty() {
        // stdin에서 읽기
        let mut buffer = String::new();
        io::stdin().read_to_string(&mut buffer).expect("Failed to read from stdin");
        buffer
    } else {
        args.join(" ")
    };
    
    if text.trim().is_empty() {
        eprintln!("Usage: ko-morph <text>");
        eprintln!("   or: echo 'text' | ko-morph");
        std::process::exit(1);
    }
    
    let analyzer = Analyzer::new();
    println!("{}", analyzer.analyze_str(&text));
}
