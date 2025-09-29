use regex::Regex;

pub fn tokenize(s: &str) -> Vec<String> {
    let re = Regex::new(
        r"[가-힣]+|[A-Za-z]+|\d+|[.,!?;:\"'()\[\]{}<>@#$%^&*+=|\\~`\-–—·…/]|[^ \t\r\n]"
    ).unwrap();
    
    let mut tokens = Vec::new();
    for m in re.find_iter(s) {
        let token = m.as_str();
        // 한글 뒤에 마침표가 붙은 경우 분리
        if token.len() > 1 && matches!(token.chars().last(), Some('.') | Some('!') | Some('?')) {
            let first_char = token.chars().next().unwrap();
            if first_char >= '가' && first_char <= '힣' {
                tokens.push(token[..token.len()-1].to_string());
                tokens.push(token[token.len()-1..].to_string());
                continue;
            }
        }
        tokens.push(token.to_string());
    }
    
    tokens
}