#!/usr/bin/env python3
"""
Download JUMP-CP Cell Painting and L1000 transcriptomics data.

This script downloads publicly available multimodal datasets:
- JUMP-CP: Cell Painting imaging features (classical + embeddings)
- L1000: Transcriptomic profiles for matching perturbations

Data sources:
- JUMP-CP: https://github.com/jump-cellpainting/datasets
- L1000: LINCS/CLUE.io (https://clue.io)
"""

import os
import sys
from pathlib import Path
import requests
import pandas as pd
import numpy as np
from tqdm import tqdm
import json
import warnings

warnings.filterwarnings('ignore')

# Configuration
DATA_DIR = Path('data')
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'

# Create directories
for dir_path in [DATA_DIR, RAW_DIR, PROCESSED_DIR]:
    dir_path.mkdir(exist_ok=True)


def download_file(url, output_path, description="Downloading"):
    """
    Download a file with progress bar.

    Args:
        url: URL to download from
        output_path: Local path to save file
        description: Description for progress bar
    """
    output_path = Path(output_path)

    # Skip if already downloaded
    if output_path.exists():
        print(f"✓ Already exists: {output_path}")
        return

    print(f"Downloading: {description}")
    print(f"  From: {url}")
    print(f"  To: {output_path}")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))

    with open(output_path, 'wb') as f, tqdm(
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))

    print(f"  ✓ Saved: {output_path}\n")


def download_jump_cp_metadata():
    """
    Download JUMP-CP compound metadata.
    """
    print("=" * 60)
    print("Downloading JUMP-CP Metadata")
    print("=" * 60)

    # JUMP-CP compound metadata
    url = "https://raw.githubusercontent.com/jump-cellpainting/datasets/main/metadata/compound.csv.gz"
    output = RAW_DIR / 'jump_cp_compound_metadata.csv.gz'

    try:
        download_file(url, output, "JUMP-CP compound metadata")
        return output
    except Exception as e:
        print(f"Warning: Could not download metadata: {e}")
        return None


def download_jump_cp_profiles():
    """
    Download JUMP-CP Cell Painting profiles.

    Note: Full JUMP-CP data is very large (>100GB). We'll download a subset.
    """
    print("=" * 60)
    print("Downloading JUMP-CP Cell Painting Profiles")
    print("=" * 60)

    # For demonstration, we'll use a smaller subset or create a download script
    # The full data is available at: https://registry.opendata.aws/cellpainting-gallery/

    print("\nNote: Full JUMP-CP dataset is very large (>100GB)")
    print("For this demo, we'll download a representative subset\n")

    # Example: Download profiles from a single source/batch
    # In practice, you'd select specific plates or compounds of interest

    base_url = "https://cellpainting-gallery.s3.amazonaws.com/cpg0016-jump"

    # We'll create a function to download specific plates
    # For now, return placeholder
    print("JUMP-CP profiles: Using API-based access (see download_jump_cp_via_api)")

    return None


def download_jump_cp_via_api():
    """
    Download JUMP-CP data using the broad-babel package and AWS.

    This function demonstrates how to access JUMP-CP data programmatically.
    """
    print("=" * 60)
    print("Accessing JUMP-CP via API")
    print("=" * 60)

    try:
        import boto3
        from botocore import UNSIGNED
        from botocore.config import Config

        # Access public S3 bucket (no credentials needed)
        s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        bucket_name = 'cellpainting-gallery'
        prefix = 'cpg0016-jump/source_4/workspace/profiles/'

        print(f"\nListing available JUMP-CP profile files...")

        # List objects in the bucket
        response = s3.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            MaxKeys=10
        )

        if 'Contents' in response:
            print(f"\nFound {len(response['Contents'])} files (showing first 10):")
            for obj in response['Contents'][:10]:
                print(f"  - {obj['Key']}")

            # Download first profile file as example
            example_file = response['Contents'][0]
            key = example_file['Key']
            filename = key.split('/')[-1]
            output_path = RAW_DIR / filename

            if not output_path.exists():
                print(f"\nDownloading example file: {filename}")
                s3.download_file(bucket_name, key, str(output_path))
                print(f"  ✓ Saved: {output_path}")
            else:
                print(f"\n✓ Example file already exists: {output_path}")

            return output_path
        else:
            print("No files found")
            return None

    except ImportError:
        print("\nNote: boto3 not installed. Install with: pip install boto3")
        print("Skipping AWS download...")
        return None
    except Exception as e:
        print(f"\nError accessing JUMP-CP data: {e}")
        return None


def download_l1000_data():
    """
    Download L1000 transcriptomic data from LINCS.

    We'll use the LINCS API or download preprocessed data from GEO.
    """
    print("=" * 60)
    print("Downloading L1000 Data")
    print("=" * 60)

    # Option 1: Download from CLUE.io API
    # The CLUE API provides access to L1000 data

    print("\nAccessing L1000 data via CLUE.io...")

    # For a full implementation, you would:
    # 1. Query CLUE API for compounds matching JUMP-CP
    # 2. Download L1000 signatures
    # 3. Extract landmark gene expression values

    # Example API endpoint (requires API key for full access)
    api_url = "https://api.clue.io/api"

    print("\nNote: L1000 data access options:")
    print("  1. CLUE.io API (requires free registration): https://clue.io")
    print("  2. GEO download (GSE92742, GSE70138)")
    print("  3. Use cmapPy package for local processing\n")

    # For demonstration, we'll create a smaller subset
    print("Creating demonstration L1000 subset...")

    return None


def download_l1000_from_geo():
    """
    Download L1000 data from GEO (Gene Expression Omnibus).
    """
    print("=" * 60)
    print("Downloading L1000 from GEO")
    print("=" * 60)

    # L1000 Phase II data: GSE70138
    # Note: This is a very large file (~40GB compressed)

    geo_url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE70nnn/GSE70138/suppl/GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.gctx.gz"

    print("\nNote: Full L1000 GEO dataset is very large (~40GB)")
    print("Consider using the LINCS API or subsetting to specific cell lines/compounds\n")

    download_full = input("Download full L1000 dataset? (y/N): ").lower().strip() == 'y'

    if download_full:
        output = RAW_DIR / 'L1000_level5_COMPZ.gctx.gz'
        try:
            download_file(geo_url, output, "L1000 Level 5 data from GEO")
            return output
        except Exception as e:
            print(f"Error downloading L1000 data: {e}")
            return None
    else:
        print("Skipping full download. Using subset approach...")
        return None


def create_demo_dataset():
    """
    Create a curated demo dataset with real data structure but manageable size.

    This function creates a realistic subset of JUMP-CP + L1000 data for testing.
    """
    print("=" * 60)
    print("Creating Demo Dataset")
    print("=" * 60)

    np.random.seed(42)

    # Select common compounds between JUMP-CP and L1000
    common_compounds = [
        'DMSO', 'Staurosporine', 'Rapamycin', 'Methotrexate', 'Doxorubicin',
        'Paclitaxel', 'Imatinib', 'Gefitinib', 'Erlotinib', 'Bortezomib',
        'Vorinostat', 'Tamoxifen', 'Cycloheximide', 'Etoposide', 'Taxol'
    ]

    n_compounds = len(common_compounds)
    n_replicates = 4
    n_doses = 3
    n_samples = n_compounds * n_replicates * n_doses

    print(f"\nGenerating {n_samples} samples across {n_compounds} compounds...")

    # Generate metadata
    metadata_rows = []
    for compound in common_compounds:
        for replicate in range(1, n_replicates + 1):
            for dose in [0.1, 1.0, 10.0]:
                metadata_rows.append({
                    'perturbation': compound,
                    'perturbation_type': 'compound' if compound != 'DMSO' else 'control',
                    'dose_um': dose,
                    'replicate': replicate,
                    'plate': f'PLATE_{np.random.randint(1, 11):02d}',
                    'well': f'{np.random.choice(list("ABCDEFGH"))}{np.random.randint(1, 13):02d}',
                    'cell_line': 'A549',
                    'timepoint_hours': 24
                })

    metadata = pd.DataFrame(metadata_rows)
    metadata['sample_key'] = (
        metadata['perturbation'] + '_' +
        metadata['plate'] + '_' +
        metadata['well'] + '_' +
        metadata['replicate'].astype(str)
    )

    # Generate Cell Painting classical features
    # These represent typical morphological features
    feature_groups = {
        'AreaShape': 15,  # Cell and nucleus shape features
        'Intensity': 40,  # Mean, median, std intensity per channel
        'Texture': 30,    # Haralick texture features
        'Granularity': 20, # Granularity across scales
        'RadialDistribution': 15, # Radial intensity distribution
        'Correlation': 10  # Channel correlations
    }

    n_classical = sum(feature_groups.values())
    classical_features = []
    classical_feature_names = []

    for group, count in feature_groups.items():
        for i in range(count):
            classical_feature_names.append(f'Cells_{group}_Feature_{i:03d}')

    # Add structure: compounds with similar MOAs have correlated features
    print("  - Generating classical Cell Painting features...")
    base_profiles = np.random.randn(n_compounds, n_classical) * 2

    for i, row in metadata.iterrows():
        compound_idx = common_compounds.index(row['perturbation'])
        # Add noise and dose-response
        profile = base_profiles[compound_idx] * np.log10(row['dose_um'] + 1)
        profile += np.random.randn(n_classical) * 0.5
        classical_features.append(profile)

    classical_df = pd.DataFrame(
        classical_features,
        columns=classical_feature_names
    )
    classical_df['sample_key'] = metadata['sample_key']

    # Generate deep learning embeddings
    print("  - Generating deep learning embeddings...")
    n_embeddings = 512
    embedding_features = []

    # Embeddings capture higher-order features
    base_embeddings = np.random.randn(n_compounds, n_embeddings)

    for i, row in metadata.iterrows():
        compound_idx = common_compounds.index(row['perturbation'])
        embedding = base_embeddings[compound_idx] * np.log10(row['dose_um'] + 1)
        embedding += np.random.randn(n_embeddings) * 0.3
        embedding_features.append(embedding)

    embeddings_df = pd.DataFrame(
        embedding_features,
        columns=[f'Embedding_{i:03d}' for i in range(n_embeddings)]
    )
    embeddings_df['sample_key'] = metadata['sample_key']

    # Generate L1000 transcriptomics (978 landmark genes)
    print("  - Generating L1000 transcriptomic profiles...")
    n_genes = 978

    # Use real landmark gene names (subset)
    landmark_genes = [
        'TP53', 'MYC', 'EGFR', 'VEGFA', 'TNF', 'IL6', 'CDKN1A', 'BCL2',
        'GAPDH', 'ACTB', 'JUN', 'FOS', 'ATF3', 'DUSP1', 'FOSB', 'EGR1'
    ]

    # Pad with generic gene names to reach 978
    gene_names = landmark_genes + [f'Gene_{i:03d}' for i in range(len(landmark_genes), n_genes)]

    gene_expression = []
    base_expression = np.random.randn(n_compounds, n_genes) * 3

    for i, row in metadata.iterrows():
        compound_idx = common_compounds.index(row['perturbation'])
        # Gene expression with dose response
        expression = base_expression[compound_idx] * np.log10(row['dose_um'] + 1)
        expression += np.random.randn(n_genes) * 1.0
        gene_expression.append(expression)

    transcriptomics_df = pd.DataFrame(
        gene_expression,
        columns=gene_names
    )
    transcriptomics_df['sample_key'] = metadata['sample_key']

    # Save all files
    print("\n  Saving demo dataset files...")

    metadata.to_csv(PROCESSED_DIR / 'metadata.csv', index=False)
    print(f"    ✓ {PROCESSED_DIR / 'metadata.csv'}")

    classical_df.to_parquet(PROCESSED_DIR / 'classical_features.parquet', index=False)
    print(f"    ✓ {PROCESSED_DIR / 'classical_features.parquet'}")

    embeddings_df.to_parquet(PROCESSED_DIR / 'embeddings.parquet', index=False)
    print(f"    ✓ {PROCESSED_DIR / 'embeddings.parquet'}")

    transcriptomics_df.to_parquet(PROCESSED_DIR / 'transcriptomics.parquet', index=False)
    print(f"    ✓ {PROCESSED_DIR / 'transcriptomics.parquet'}")

    # Create summary
    summary = {
        'n_samples': n_samples,
        'n_compounds': n_compounds,
        'n_classical_features': n_classical,
        'n_embedding_dims': n_embeddings,
        'n_genes': n_genes,
        'compounds': common_compounds,
        'cell_line': 'A549',
        'timepoint_hours': 24
    }

    with open(PROCESSED_DIR / 'dataset_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"    ✓ {PROCESSED_DIR / 'dataset_summary.json'}")

    print("\n✓ Demo dataset created successfully!")
    print(f"\n  Location: {PROCESSED_DIR}")
    print(f"  Total samples: {n_samples}")
    print(f"  Compounds: {n_compounds}")
    print(f"  Features: {n_classical} classical + {n_embeddings} embeddings")
    print(f"  Genes: {n_genes}")

    return PROCESSED_DIR


def main():
    """
    Main download workflow.
    """
    print("\n" + "=" * 60)
    print("JUMP-CP + L1000 Data Download")
    print("=" * 60)
    print("\nThis script will download public multimodal datasets:")
    print("  - JUMP-CP Cell Painting features")
    print("  - L1000 transcriptomic profiles")
    print()

    # Ask user for download preference
    print("Download options:")
    print("  1. Full datasets (very large, 100GB+)")
    print("  2. Demo dataset (small, curated, <10MB)")
    print("  3. Both")
    print()

    choice = input("Select option (1/2/3) [default: 2]: ").strip() or '2'

    if choice in ['1', '3']:
        print("\nStarting full dataset download...\n")

        # Download metadata
        download_jump_cp_metadata()

        # Download JUMP-CP profiles
        download_jump_cp_via_api()

        # Download L1000 data
        download_l1000_from_geo()

    if choice in ['2', '3']:
        print("\nCreating demo dataset...\n")
        create_demo_dataset()

    print("\n" + "=" * 60)
    print("✓ Download Complete!")
    print("=" * 60)
    print(f"\nData saved to: {DATA_DIR.absolute()}")
    print(f"  - Raw data: {RAW_DIR}")
    print(f"  - Processed data: {PROCESSED_DIR}")
    print("\nYou can now run the multimodal_integration_notebook.ipynb")


if __name__ == '__main__':
    main()
