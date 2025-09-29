use crate::dicts::AffixDicts;

pub type Cand = Vec<(String, String)>;

pub fn generate_candidates(token: &str, aff: &AffixDicts) -> Vec<Cand> {
    let mut out: Vec<Cand> = Vec::new();
    
    // Baseline: 명사
    out.push(vec![(token.to_string(), "N".into())]);
    
    // 한글이 아니면 특수 처리
    if !token.chars().any(|c| c >= '가' && c <= '힣') {
        if token.chars().all(|c| c.is_ascii_digit()) {
            out[0] = vec![(token.to_string(), "NUM".into())];
        } else if token.chars().all(|c| c.is_ascii_alphabetic()) {
            out[0] = vec![(token.to_string(), "ENG".into())];
        } else if matches!(token.as_str(), "." | "!" | "?") {
            out[0] = vec![(token.to_string(), "SF".into())];
        } else if matches!(token.as_str(), "," | ";" | ":") {
            out[0] = vec![(token.to_string(), "SP".into())];
        }
        return out;
    }
    
    // 어미 분해 시도 (우선)
    for suf in &aff.eomi_sorted {
        if token.len() > suf.len() && token.ends_with(suf) {
            let stem = &token[..token.len() - suf.len()];
            if !stem.is_empty() {
                out.push(vec![
                    (stem.to_string(), "V".into()),
                    ((*suf).to_string(), "E".into())
                ]);
                break;
            }
        }
    }
    
    // 조사 분해 시도
    for suf in &aff.josa_sorted {
        if token.len() > suf.len() && token.ends_with(suf) {
            let stem = &token[..token.len() - suf.len()];
            if !stem.is_empty() {
                out.push(vec![
                    (stem.to_string(), "N".into()),
                    ((*suf).to_string(), "J".into())
                ]);
                break;
            }
        }
    }
    
    out
}