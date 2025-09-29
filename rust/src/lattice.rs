#[derive(Clone)]
pub struct CandidatePath {
    pub token_idx: usize,
    pub analysis: super::rules::Cand,
    pub local_score: f32,
}

pub struct Lattice {
    pub layers: Vec<Vec<CandidatePath>>,
}

impl Lattice {
    pub fn new() -> Self {
        Self { layers: Vec::new() }
    }
    
    pub fn add_layer(&mut self, cands: Vec<CandidatePath>) {
        self.layers.push(cands);
    }
    
    pub fn best_path(&self) -> Vec<CandidatePath> {
        self.layers
            .iter()
            .filter_map(|layer| {
                layer.iter()
                    .max_by(|a, b| a.local_score.partial_cmp(&b.local_score).unwrap())
                    .cloned()
            })
            .collect()
    }
}
