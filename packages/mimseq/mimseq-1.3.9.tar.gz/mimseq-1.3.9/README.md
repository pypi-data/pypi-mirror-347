<p align="center">
	<img src="docs/img/globular_multi.png" width="450" height="450">
</p>

# mim-tRNAseq
[![Documentation Status](https://readthedocs.org/projects/mim-trnaseq/badge/?version=latest)](https://mim-trnaseq.readthedocs.io/en/latest/?badge=latest)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6782628.svg)](https://doi.org/10.5281/zenodo.6782628)

**Original paper** - https://doi.org/10.1016/j.molcel.2021.01.028

**Protocol paper** - https://doi.org/10.1016/j.xpro.2022.101579

### Modification-induced misincorporation tRNA sequencing.

This package is an automated analysis pipeline for the quantitation and analysis of tRNA expression and modifications. Given trimmed sequencing reads in fastq format, this pipeline will:
* Cluster tRNAs, index modifications, and perform SNP-tolerant read alignment with [GSNAP](http://research-pub.gene.com/gmap/)
* Deconvolve cluster aligned reads back into unique tRNA transcript-level reads
* Calculate coverage information and plots (useful for QC)
* Quantify expression
* Calculate tRNA differential expression with [DESeq2](https://bioconductor.org/packages/release/bioc/html/DESeq2.html).
* Analyze functional tRNA pools and tRNA completeness via 3'-CCA analysis
* Comprehensive modification quantification and misincorporation signature analysis
* Detect coordination between pairs of modifications and modification-aminoacylation with [SLAC](https://doi.org/10.1093/nar/gkac1185) (SingLe-read Analysis of Crosstalks)

## Method strategy

Detailed methodology is shown in the image below, and described in Behrens et al. (2020)

![methods](/docs/img/method.png)

 
## Installation and usage

[![Documentation Status](https://readthedocs.org/projects/mim-trnaseq/badge/?version=latest)](https://mim-trnaseq.readthedocs.io/en/latest/?badge=latest)

Please see the full documentation for explanations of dependencies, inputs formatting, and outputs.

To use mim-tRNAseq, it is recommended to install the package using `conda`, preferably in its own environment. Significant time and dependency-related improvements can be made to using conda for managing environment and installing mimseq using the [Miniforge](https://github.com/conda-forge/miniforge) version of conda which oncludes optional use for Mamba. We recommend installing Miniforge and then following the steps below:
```bash
	conda create -n mimseq python=3.7
	conda activate mimseq
	mamba install -c bioconda mimseq
```

usearch needs to be acquired and installed. Please do the following:
```bash
	wget https://drive5.com/downloads/usearch10.0.240_i86linux32.gz
	gunzip usearch10.0.240_i86linux32.gz
	chmod +x usearch10.0.240_i86linux32
	mv usearch10.0.240_i86linux32 usearch
	cp usearch /usr/local/bin
```
For this last cp command, root access is required. However, if this is not possible, please add the path to the usearch binary to your PATH (replace `full/path/to/usearch` with location of your usearch binary from above:
```bash
export PATH=$PATH:full/path/to/usearch
```

Alternatively, mim-tRNAseq can be installed with `pip`, in which case all additional non-python package dependencies (including `usearch` as above, `BLAST`, `infernal`, `GMAP/GSNAP`, and all required R packages) will also need to be installed manually.
```bash
	pip install mimseq
```

Once installed, mim-tRNAseq should be executable and help displayed, by running
```bash
	mimseq --help
```
An example command to run mim-tRNAseq may look as follows. This will run an analysis between HEK293T and K562 cells on an example dataset included in the package:
```bash
	mimseq --species Hsap --cluster-id 0.97 --threads 15 --min-cov 0.0005 --max-mismatches 0.075 --control-condition HEK293T -n hg38_test --out-dir hg38_HEK239vsK562 --max-multi 4 --remap --remap-mismatches 0.05 sampleData_HEKvsK562.txt
```
The run should take around 15 minutes on a server using 15 processors (`--threads 15`: please update according to your server capabilities).

To run the [SingLe-read Analysis of Crosstalks (SLAC)](https://doi.org/10.1093/nar/gkac1185) between tRNA modifications and aminoacylation, specify the optional argument `--crosstalks`. The run can take a few minutes longer depending on the number of processors.
```bash
	mimseq --species Hsap --cluster-id 0.97 --threads 15 --min-cov 0.0005 --max-mismatches 0.075 --control-condition HEK293T -n hg38_test --out-dir hg38_HEK239vsK562 --max-multi 4 --remap --remap-mismatches 0.05 --crosstalks sampleData_HEKvsK562.txt
```

## Contact

Please log all issues/suggestions on the mim-tRNAseq GitHub page: https://github.com/nedialkova-lab/mim-tRNAseq/issues

Drew Behrens: abehrens@biochem.mpg.de

Danny Nedialkova: nedialkova@biochem.mpg.de

Nedialkova laboratory: https://www.biochem.mpg.de/nedialkova


## Cite

Behrens et al., 2021, High-resolution quantitative profiling of tRNA abundance and modification status in eukaryotes by mim-tRNaseq. Molecular Cell 81, 1–14 (https://doi.org/10.1016/j.molcel.2021.01.028)

Behrens and Nedialkova, 2022, Experimental and computational workflow for the analysis of tRNA pools from eukaryotic cells by mim-tRNAseq. STAR Protocols. 3, 101579 (https://doi.org/10.1016/j.xpro.2022.101579)
