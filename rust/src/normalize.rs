use unicode_normalization::UnicodeNormalization;

pub fn normalize(s: &str) -> String {
    let nfc: String = s.nfc().collect();
    let mut out = String::with_capacity(nfc.len());
    let mut last_space = false;
    
    for ch in nfc.chars() {
        if ch.is_whitespace() {
            if !last_space {
                out.push(' ');
            }
            last_space = true;
        } else {
            last_space = false;
            out.push(ch);
        }
    }
    
    out.trim().to_string()
}
