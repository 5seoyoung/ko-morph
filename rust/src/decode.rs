use crate::{
    lattice::{CandidatePath, Lattice},
    rules::Cand,
    scorer::score_candidate,
};

pub fn decode_sentence(token_candidates: &[Vec<Cand>]) -> Vec<Cand> {
    let mut lat = Lattice::new();
    
    for (i, cands) in token_candidates.iter().enumerate() {
        let layer: Vec<CandidatePath> = cands
            .iter()
            .map(|c| {
                let s = score_candidate(c);
                CandidatePath {
                    token_idx: i,
                    analysis: c.clone(),
                    local_score: s,
                }
            })
            .collect();
        lat.add_layer(layer);
    }
    
    lat.best_path()
        .into_iter()
        .map(|cp| cp.analysis)
        .collect()
}