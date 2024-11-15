
# MineGraph: Plant Plastid-Mitochondria Pangenome-Graph Analysis Tool

**Overview**  
MineGraph is a streamlined bioinformatics tool designed to generate, analyze, and visualize pangenome graphs specifically for plant plastid and mitochondria genomes. It simplifies the complex processes of graph creation and statistical analysis, offering a comprehensive solution for comparative genomics and variation detection across sequences.

### Key Terminology

- **Graph**: A data structure where nodes (vertices) represent entities, and edges define relationships between them.
- **Variation Graph**: A non-overlapping sequence graph where nodes represent sequence segments and edges show connections, useful in identifying genetic variations.
- **Pangenome Variation Graph**: A form of generic multiple sequence alignment. It reveals similarities where genomes traverse the same parts of the graph and differences where they do not.
- **PGGB (PanGenome Graph Builder)**: A tool used to build pangenome graphs from sequence data.
- **PanSN-spec**: A naming convention for labeling sequences in a pangenome, retaining this information across formats.
- **GFA (Graphical Fragment Assembly) Format**: A format used to represent sequence graphs.

### Description

MineGraph is a user-friendly bioinformatics tool designed to automate the workflow of pangenome graph analysis. With Docker support, it operates in a contained environment, eliminating complex installation steps. MineGraph takes an input set of sequences and performs a detailed pre-analysis to optimize parameters, minimizing manual intervention and ensuring that the resulting pangenome graph is accurate and informative.

### Key Functionalities and Advantages

1. **Automated Parameter Optimization**  
   MineGraph extracts and optimizes critical parameters, such as **mapping identity minimum (-p)** and **segment length (-s)**, which are essential for accurate graph construction. This automation ensures optimal graph structure, streamlining the process with minimal configuration.

   - **Maximum Divergence Calculation**: Using MASH Triangle, MineGraph calculates the ideal percentage identity, representing the divergence among input sequences.
   - **Handling Repetitive Regions**: Transposable elements and repetitive sequences are common in plant genomes, complicating pangenome analysis. MineGraph uses RepeatMasker to identify the longest tandem repeats (TRs) and sets this as the segment length for PGGB, improving graph accuracy in repetitive regions.

2. **Sequence Preparation and Compression**  
   MineGraph organizes, renames, and compresses sequences following the PanSN-spec convention. The compressed and indexed files serve as streamlined inputs for PGGB, enabling consistent and traceable sequence naming across formats.

3. **Comprehensive Graph Analysis and Outputs**  
   Once the pangenome graph is generated, MineGraph performs a robust statistical analysis and generates a variety of outputs, including:
   - **Graph Statistics**: Details like node and edge counts, and average node degree.
   - **Polymorphism Summary**: A VCF file summarizing Single Nucleotide Polymorphisms (SNPs), Multiple Nucleotide Polymorphisms (MNPs), and indels.
   - **Graph Visualization**: A circular plot where node size reflects sequence size, and edge width represents connection weight.
   - **Node Count Histogram**: A histogram representing node count distribution across the graph.
   - **Metrics Dataframes**: Detailed data including node IDs, counts, and sizes.
   - **Consensus Sequence**: The derived consensus sequence of the graph.
   - **Multiple Sequence Alignment (MSA)**: Alignment file reflecting the consensus across input sequences.
   - **Phylogenetic Tree**: A tree showing evolutionary relationships based on the pangenome graph.
   - **GFA Conversion**: Conversion of GFA format into FASTA and VG for compatibility with additional tools.

4. **Docker Integration**  
   MineGraph is designed to run in a Docker container, simplifying setup by eliminating software dependency issues. It’s compatible with most systems, making it accessible to users without requiring extensive technical expertise.

### System Requirements

- **10 GB free disk space**
- **Docker installed**
- **Python installed with pandas package**

### Getting Started

To start using MineGraph, create a CSV or XLSX file listing the names of your FASTA files with a column named `fasta_files`. Example:

```plaintext
fasta_files
Avena_sativa.fasta
Triticum.fasta
Zea_Mays.fasta
...
```

Place the FASTA files in a folder (e.g., `./my_data/`) in the current directory, then provide the folder as an argument when running MineGraph.

### Usage

```bash
python MineGraph.py <data_dir> [input_file] [threads]
```

- **Arguments:**
  - `<data_dir>`: Directory containing the raw FASTA files. The results will be saved here.
  - `[input_file]`: (Optional) CSV or XLSX file listing the FASTA files to process. If omitted, all FASTA files in `<data_dir>` will be used.
  - `[threads]`: (Optional) Number of threads for PGGB and other parallel tasks. Default is 16.

- **Examples:**
  ```bash
  # Run MineGraph with a list of selected FASTA files
  python MineGraph.py /path/to/your/data selected_files.csv 

  # Run MineGraph with 64 threads
  python MineGraph.py /path/to/your/data selected_files.csv 64   
  ```

The final output will be organized in the following folders:
- `/path/to/your/data/MineGraph_output`: Contains the pipeline’s final output files.
- `/path/to/your/data/pggb_output`: Includes the GFA file, VCF file, and an ODGI drawing of the final graph.

---

MineGraph provides a powerful, efficient approach to analyzing plant plastid and mitochondria genomes, equipping researchers with optimized pangenome graphs and comprehensive statistics for their genomic studies.
