# Multimodal Integration: Imaging + Transcriptomics

A complete Python workflow for integrating high-content imaging (Cell Painting) features with transcriptomic profiles (L1000) using public datasets.

## Overview

This project demonstrates multimodal data integration using:
- **JUMP-CP**: Cell Painting imaging features (classical morphological + deep learning embeddings)
- **L1000**: Transcriptomic profiles for matching perturbations

The workflow implements three complementary analysis methods:
1. **Correlation Analysis**: Make embeddings interpretable by linking to classical features
2. **Partial Least Squares (PLS)**: Find latent components maximizing covariance between modalities
3. **Multi-Omics Factor Analysis (MOFA2)**: Discover shared and modality-specific variation

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/arudhir/mofa-deez.git
cd mofa-deez

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download Data

Run the data download script to get JUMP-CP and L1000 data:

```bash
python download_data.py
```

**Options:**
- **Option 1**: Full datasets (large, 100GB+) - downloads real JUMP-CP and L1000 data
- **Option 2**: Demo dataset (small, <10MB) - creates curated synthetic data for testing
- **Option 3**: Both

For quick testing, choose **Option 2** (demo dataset).

### 3. Run Analysis

Open and run the Jupyter notebook:

```bash
jupyter notebook multimodal_integration_notebook.ipynb
```

Or using JupyterLab:

```bash
jupyter lab multimodal_integration_notebook.ipynb
```

Run all cells sequentially (Cell → Run All) to perform the complete analysis.

## Project Structure

```
mofa-deez/
├── README.md                              # This file
├── requirements.txt                       # Python dependencies
├── download_data.py                       # Data download script
├── multimodal_integration_notebook.ipynb  # Main analysis notebook
├── data/                                  # Data directory (created by download script)
│   ├── raw/                              # Raw downloaded files
│   └── processed/                        # Processed data files
│       ├── metadata.csv
│       ├── classical_features.parquet
│       ├── embeddings.parquet
│       └── transcriptomics.parquet
└── outputs/                               # Analysis outputs (created by notebook)
    ├── data/                             # Processed matrices and results
    ├── figures/                          # Visualizations
    └── models/                           # Saved MOFA2 models
```

## Data Sources

### JUMP-CP (Cell Painting)
- **Source**: [JUMP Cell Painting Consortium](https://github.com/jump-cellpainting/datasets)
- **AWS S3**: `s3://cellpainting-gallery/cpg0016-jump/`
- **Features**:
  - Classical morphological features (~1,780 dimensions)
  - Deep learning embeddings (512 dimensions)
  - Metadata: compound, dose, plate, well, replicate

### L1000 (Transcriptomics)
- **Source**: [LINCS/CLUE.io](https://clue.io)
- **GEO**: GSE92742, GSE70138
- **Features**:
  - 978 landmark genes
  - z-scored differential expression values
  - Cell line: A549 (lung cancer)

## Analysis Workflow

### 1. Data Loading
- Load imaging features (classical + embeddings)
- Load L1000 gene expression profiles
- Load metadata (perturbation, dose, plate, well, replicate)

### 2. Metadata Alignment
- Build unique sample keys from metadata
- Align all modalities to common samples
- Verify data integrity

### 3. Preprocessing
- Remove NA features (>5% missing)
- Filter low-variance features
- Z-score normalization across samples

### 4. Correlation Analysis
- Compute correlation matrix: embeddings × classical features
- Hierarchical clustering heatmap
- Identify interpretable embedding dimensions

### 5. PLS Integration
- Concatenate imaging features
- Optional PCA reduction of transcriptomics
- Fit PLS with 5 components
- Extract latent scores and loadings
- Plot variance explained and biplots

### 6. MOFA2 Integration
- Configure 2-view model (imaging, transcriptomics)
- Train with 10 factors
- Extract factor matrix and weights
- Compute variance explained per view
- Analyze factor-metadata associations

### 7. Outputs
- Aligned feature matrices (parquet)
- Correlation heatmaps (PNG)
- PLS scores and loadings (CSV)
- MOFA2 factors and weights (CSV)
- Interpretation summary (CSV)

## Output Files

### Data Files (`outputs/data/`)
- `aligned_imaging_matrix.parquet` - Combined classical + embeddings
- `aligned_transcriptomics_matrix.parquet` - Gene expression matrix
- `sample_metadata.csv` - Sample metadata
- `embedding_interpretation.csv` - Embedding-feature correlations
- `pls_scores.csv` - PLS latent component scores
- `pls_loadings.csv` - PLS feature loadings
- `mofa_factors.csv` - MOFA2 factor values per sample
- `mofa_weights_imaging.csv` - MOFA2 weights for imaging view
- `mofa_weights_transcriptomics.csv` - MOFA2 weights for transcriptomics view
- `summary_embedding_biology.csv` - Biological interpretation summary

### Figures (`outputs/figures/`)
- `correlation_clustermap.png` - Embedding-classical feature correlations
- `pls_variance_explained.png` - PLS variance explained
- `pls_biplots.png` - PLS score plots
- `mofa_variance_explained.png` - MOFA2 variance per factor
- `mofa_factor_heatmap.png` - MOFA2 factor heatmap
- `pls_mofa_comparison.png` - Cross-method comparison

## Customization

### Using Your Own Data

To adapt this workflow to your own HCI + RNA-seq data:

1. **Prepare your data files** in the same format:
   ```python
   # metadata.csv
   perturbation, plate, well, replicate, dose_um, ...

   # classical_features.parquet
   sample_key, Feature_1, Feature_2, ...

   # embeddings.parquet
   sample_key, Embedding_1, Embedding_2, ...

   # transcriptomics.parquet
   sample_key, Gene_1, Gene_2, ...
   ```

2. **Modify data loading** in the notebook:
   ```python
   # In cell 4, replace load_data_files() with your loader
   def load_my_data():
       metadata = pd.read_csv('path/to/my_metadata.csv')
       classical = pd.read_parquet('path/to/my_features.parquet')
       # ... etc
   ```

3. **Adjust preprocessing parameters**:
   - NA threshold (default: 5%)
   - Variance threshold (default: 0.01)
   - Number of PLS components (default: 5)
   - Number of MOFA factors (default: 10)

### Analysis Parameters

Key parameters you can modify in the notebook:

```python
# Preprocessing
NA_THRESHOLD = 0.05  # Maximum NA fraction
VARIANCE_THRESHOLD = 0.01  # Minimum variance

# PLS
N_PLS_COMPONENTS = 5
USE_PCA_REDUCTION = True  # Reduce transcriptomics before PLS
N_PCA_COMPONENTS = 200

# MOFA2
N_MOFA_FACTORS = 10
MOFA_ITERATIONS = 1000
```

## Requirements

- Python 3.8+
- 8GB+ RAM (for demo dataset)
- 32GB+ RAM (for full JUMP-CP dataset)
- 50GB+ disk space (for full datasets)

## Troubleshooting

### MOFA2 Installation Issues

If you encounter issues installing MOFA2:

```bash
# Install from conda-forge (recommended)
conda install -c conda-forge mofapy2

# Or install dependencies separately
pip install h5py pandas numpy scipy
pip install mofapy2
```

### Memory Issues

For large datasets:

1. **Subsample features** before analysis:
   ```python
   # In notebook, after loading data
   classical_features = classical_features.iloc[:, :500]  # Use first 500 features
   ```

2. **Use PCA reduction**:
   ```python
   USE_PCA_REDUCTION = True
   N_PCA_COMPONENTS = 100  # Reduce to 100 components
   ```

3. **Process in batches**:
   ```python
   # Compute correlations in batches
   batch_size = 100
   for i in range(0, n_features, batch_size):
       corr_batch = compute_correlation(features[i:i+batch_size])
   ```

### AWS Access Issues

If downloading from AWS S3 fails:

1. **Check network connection**
2. **Install/update boto3**:
   ```bash
   pip install --upgrade boto3
   ```
3. **Use demo dataset** instead (Option 2 in download script)

## Citation

If you use this workflow in your research, please cite:

**JUMP-CP:**
```
Chandrasekaran, S.N., et al. (2022).
JUMP Cell Painting dataset: morphological impact of 136,000 chemical and genetic perturbations.
bioRxiv. https://doi.org/10.1101/2022.01.05.475090
```

**L1000:**
```
Subramanian, A., et al. (2017).
A Next Generation Connectivity Map: L1000 Platform and the First 1,000,000 Profiles.
Cell, 171(6), 1437-1452.e17. https://doi.org/10.1016/j.cell.2017.10.049
```

**MOFA2:**
```
Argelaguet, R., et al. (2020).
MOFA+: a statistical framework for comprehensive integration of multi-modal single-cell data.
Genome Biology, 21(1), 111. https://doi.org/10.1186/s13059-020-02015-1
```

## License

This project is licensed under the MIT License.

## Support

For issues or questions:
- Open an issue on [GitHub](https://github.com/arudhir/mofa-deez/issues)
- Check the [JUMP-CP documentation](https://jump-cellpainting.broadinstitute.org/)
- Visit [LINCS/CLUE.io](https://clue.io) for L1000 help

## Acknowledgments

- JUMP Cell Painting Consortium
- LINCS Program
- Broad Institute
- MOFA2 developers
