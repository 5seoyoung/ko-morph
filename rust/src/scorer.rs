use crate::rules::Cand;

pub fn score_candidate(analysis: &Cand) -> f32 {
    let mut score = 0.1;
    let tags: Vec<&str> = analysis.iter().map(|(_, t)| t.as_str()).collect();
    
    // 분해 보너스
    if tags.iter().any(|t| *t == "J" || *t == "E") {
        score += 0.5;
    }
    
    // 형태소 길이 보너스
    for (morph, pos) in analysis {
        if matches!(pos.as_str(), "N" | "V" | "A") && morph.chars().count() >= 2 {
            score += (morph.chars().count() as f32 * 0.03).min(0.2);
        }
    }
    
    // 품사 연접 보너스
    if analysis.len() == 2 {
        let (_, pos1) = &analysis[0];
        let (_, pos2) = &analysis[1];
        match (pos1.as_str(), pos2.as_str()) {
            ("N", "J") | ("V", "E") | ("A", "E") => score += 0.5,
            _ => {}
        }
    }
    
    // 은/는 모호성 처리
    if analysis.len() >= 2 {
        let (suf, tag) = &analysis[1];
        if matches!(suf.as_str(), "은" | "는") {
            if tag == "E" {
                score -= 0.4;
            } else if tag == "J" {
                score += 0.3;
            }
        }
    }
    
    // 너무 짧은 토큰 페널티
    let total_len: usize = analysis.iter().map(|(m, _)| m.chars().count()).sum();
    if total_len <= 1 {
        score -= 0.2;
    }
    
    score
}