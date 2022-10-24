import numpy as np
from scipy.stats import zscore

class attMat:
    """
    This is a special class designed for working with transformer
    attention scores, specifically with DNA sequences that have
    been parsed into k-mers. Designed to work alongside the 
    kMer class.

    === Instance Variables ===
    @pd.dataframe kmerdf: a numpy dataframe of kMer objects

    === Representation Invariants ===
    
    === Preconditions ===
    - scores is a numpy array of attention scores
    - dnadf is a numpy array of DNA sequences

    scores.shape == dnadf.shape
    """

    def __init__(self, scores, dnadf):
        scores = zscore(scores)
        self.kmerdf = self._make_kmerdf(scores, dnadf)
    
    def _make_kmerdf(self, scores, dnadf):
        """
        Creates a numpy dataframe of kMer objects from the scores and
        dnadf dataframes. The kMer objects are stored in a pandas
        dataframe for easy access and manipulation.
        """
        # TODO: I have to initialize the object with the kmers class. Might be harder to do in numpy than pandas
        kmerdf = []
        for row_idx, row_val in enumerate(scores):
            row = [] # list of kMer objects
            for col_idx, col_val in enumerate(row_val):
                kmer = kMer(row_idx, col_idx, scores[row_idx, col_idx], dnadf[row_idx, col_idx]) # create a kMer object
                row.append(kmer) # add it to the row
            kmerdf.append(row) # add the row to the dataframe
        return np.array(kmerdf)
        
    def get_kmer(self, row, col):
        """
        Returns the kMer object at the given row (ID) and column (position).
        """
        return self.kmerdf[row, col]

    def filter_kmers(self, zscore):
        """
        Filters the k-mer dataframe and returns a list of kMer objects
        satisfying the z-score threshold. 

        === Preconditions ===
        - float zscore: the z-score threshold
        """
        filtered_kmers = []
        for row in self.kmerdf:
            for kmer in row:
                if kmer.score >= zscore:
                    filtered_kmers.append(kmer)
        return filtered_kmers

    def get_kmer_instances(self, seq):
        """
        Returns a list of kMer objects the match the given sequence

        === Preconditions ===
        - str seq: the sequence to search for
        """
        kmers = []
        for row in self.kmerdf:
            for kmer in row:
                if kmer.seq == seq:
                    kmers.append(kmer)
        return kmers

    def get_contiguous_kmers(self, zscore):
        """
        Returns List[List[kMer]], where kMers satisfy the zscore 
        threshold and each List[kMer] is a contiguous high-scoring sequence.
        """
        return_list = []
        for i in range(len(self.kmerdf)):
            contiguous_kmers = []
            row = self.kmerdf[i]
            for j in range(1, len(row)-1): #start at index one, end at second to last index (to avoid index out of bounds)
                kmer = row[j]
                if kmer.score >= zscore and (row[j+1].score >= zscore or row[j-1].score >= zscore): # if the next kmer is also high scoring
                    contiguous_kmers.append(kmer) # add it to the list
            # edge cases, check the first and last kmers
            if row[0].score >= zscore and row[1].score >= zscore:
                contiguous_kmers.append(row[0])
            if row[-1].score >= zscore and row[-2].score >= zscore:
                contiguous_kmers.append(row[-1])
            return_list.append(contiguous_kmers) 
        return return_list

class kMer:
    """
    Designed for working with transformer attention matrices.
    Works in conjunction with the attMat class.

    === Instance Variables ===
    @str ID: the identifer for the DNA sequence this k-mer belongs to. 
    @int pos: the position of this k-mer in the sequence
    @int score: the attention score of this k-mer
    @string seq: the sequence of this k-mer.
    @int label: the classficiation label for this k-mer. 0 for unstable, 1 for stable.

    === Representation Invariants ===
    - 0 <= pos <= len(seq) - k
    - k > 0
    - seq is a valid DNA sequence
    """

    def __init__(self, ID, pos, score, seq, label):
        self.ID = ID
        self.pos = pos
        self.score = score
        self.seq = seq
        self.label = label

    def __str__(self):
        return f"Sequence ID: {self.ID}, Sequence: {self.seq}, Position: {self.pos}, Score: {self.score}"    
    
    
