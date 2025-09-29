pub struct AffixDicts {
    pub josa: Vec<&'static str>,
    pub eomi: Vec<&'static str>,
    pub josa_sorted: Vec<&'static str>,
    pub eomi_sorted: Vec<&'static str>,
}

fn sort_longest_first(mut v: Vec<&'static str>) -> Vec<&'static str> {
    v.sort_by(|a, b| b.len().cmp(&a.len()));
    v
}

impl AffixDicts {
    pub fn new() -> Self {
        let josa = vec![
            "은", "는", "이", "가", "을", "를", "에", "에서", "에게",
            "으로", "로", "과", "와", "보다", "의", "도", "만", "까지",
            "부터", "마다", "처럼", "치고", "한테", "께", "께서"
        ];
        
        let eomi = vec![
            "다", "요", "니다", "네요", "습니다", "합니다", "ㅂ니다",
            "고", "게", "도록", "면", "지만", "니까", "니까요",
            "는데", "는데요", "아서", "어서", "며", "며서",
            "었다", "았다", "겠다", "었어요", "았어요", "했어요",
            "습니까", "ㅂ니까", "입니까", "였어요", "라서", "이라서",
            "네", "ㄴ가요", "ㄹ까요", "ㄹ게요", "자", "죠"
        ];
        
        let josa_sorted = sort_longest_first(josa.clone());
        let eomi_sorted = sort_longest_first(eomi.clone());
        
        Self { josa, eomi, josa_sorted, eomi_sorted }
    }
}
