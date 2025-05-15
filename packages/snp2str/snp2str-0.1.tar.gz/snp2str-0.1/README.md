# SNP2STR

A Python tool for converting SNP genotype data in PED file (.ped) format to a format suitable for STRUCTURE analysis.

## Overview

SNP2STR processes genomic data files, specifically PED files (.ped) containing SNP (Single Nucleotide Polymorphism) genotype data, and converts them into a format that can be used for population structure analysis with STRUCTURE software. The tool handles the conversion of nucleotide bases to numeric codes required by STRUCTURE.

## Features

- Converts PED files (.ped) to STRUCTURE input format
- Supports optional POPULATION file (.txt) and MAP file (.map)
- Validates input data for consistency
- Handles nucleotide base coding conversion
- Provides command-line interface for easy usage
- Supports header customization in output files

## Installation

```bash
# Install from PyPI
pip install snp2str

# Or clone the repository
git clone https://github.com/vladgheorghe/snp2str.git
cd snp2str
pip install -e .
```

## Requirements

- Python 3.6+
- pandas 2.2.3

## Usage

### Command Line Interface

```bash
# Basic usage with a PED file (.ped)
snp2str path/to/your/file.ped

# Using all optional files
snp2str path/to/your/file.ped path/to/your/populations.txt path/to/your/file.map

# Specify output path
snp2str path/to/your/file.ped --output custom_output.csv

# Skip header in output file
snp2str path/to/your/file.ped --skip-output-header

# Skip first line in input PED file (.ped)
snp2str path/to/your/file.ped --skip-input-header
```

### Python API

```python
from snp2str.process import process_files

# Basic usage
process_files(ped_path="path/to/your/file.ped")

# With all options
process_files(
    ped_path="path/to/your/file.ped",
    pop_path="path/to/your/populations.txt",
    map_path="path/to/your/file.map",
    add_header=True,
    output_path="custom_output.csv",
    skip_input_header=False
)
```

## Input Files

1. **PED file (.ped)** - Required
   - Contains genotype data with SNP information
   - Each row represents an individual
   - First 6 columns contain metadata, followed by genotype data

2. **POPULATION file (.txt)** - Optional
   - Contains population information for each individual
   - One population identifier per line

3. **MAP file (.map)** - Optional
   - Contains marker information
   - Used to generate headers in the output file

## Output Format

The output is a CSV file formatted for STRUCTURE analysis:
- Each individual is represented by two rows (one for each chromosome)
- First column contains the individual identifier
- Second column contains the population identifier (if provided)
- Remaining columns contain the coded alleles

## Base Coding

SNP bases are coded according to the following scheme:
- A → 1
- T → 2
- G → 3
- C → 4
- Missing data → -9