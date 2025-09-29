pub mod normalize;
pub mod tokenize;
pub mod dicts;
pub mod rules;
pub mod lattice;
pub mod scorer;
pub mod decode;

pub struct Analyzer {
    dicts: dicts::AffixDicts,
}

impl Analyzer {
    pub fn new() -> Self {
        Self { dicts: dicts::AffixDicts::new() }
    }

    pub fn analyze_str(&self, text: &str) -> String {
        let norm = normalize::normalize(text);
        let toks = tokenize::tokenize(&norm);
        let token_cands: Vec<_> = toks.iter()
            .map(|t| rules::generate_candidates(t, &self.dicts))
            .collect();
        let best = decode::decode_sentence(&token_cands);
        
        toks.into_iter()
            .zip(best.into_iter())
            .map(|(tok, anal)| {
                let seg = anal.iter()
                    .map(|(m, t)| format!("{}/{}", m, t))
                    .collect::<Vec<_>>()
                    .join(" + ");
                format!("{}\t{}", tok, seg)
            })
            .collect::<Vec<_>>()
            .join("\n")
    }
}
