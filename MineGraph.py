import os
import sys
import pandas as pd
import subprocess

def print_help():
    print(r"""
    ============================================================
    || WELCOME TO THE MineGraph - GRAPH ANALYSIS WORKFLOW      ||
    ============================================================
    |                                                          |
    |     This workflow will take you through:                 |
    |     - FASTA preparation and compression                  |
    |     - Repeat Masker analysis for Tandem Repeats          |
    |     - PGGB alignment and graph generation                |
    |     - Graph statistical analysis                         |
    |                                                          |
    |                   Developed witH ❤️                      |
    ============================================================
    """)
    
    print("""
    HOW TO USE THIS WORKFLOW:

    Usage:
        python MineGraph.py <data_dir> [input_file] [threads]

    Arguments:
        <data_dir>   : Directory containing the raw FASTA files, where the results will be saved.
        [input_file] : CSV or XLSX file specifying the list of FASTA files to process. 
                       If not provided, all FASTA files in the <data_dir> will be used.
                       Ensure the file has a column named 'fasta_files' with filenames.
        [threads]    : (Optional) Number of threads to use for PGGB and other parallel tasks.
                       Default is 16.

    EXAMPLES:

        Example 2: Run with a CSV list of selected FASTA files
            $ python MineGraph.py /path/to/your/data selected_files.csv 

        Example 2: Run with a CSV list of selected FASTA files and 64 threads 
            $ python MineGraph.py /path/to/your/data selected_files.csv 64

    LET'S GET STARTED!
    """)

def run_workflow(data_dir, input_file=None, threads=16):
    """
    Run the full workflow with Docker, starting from the given directory.
    Accepts either a file list or all files in data_dir if no file is provided.

    Args:
        data_dir (str): Directory with FASTA files or selected files list.
        input_file (str, optional): CSV or XLSX file with list of FASTA files to process.
        threads (int): Number of threads to use for PGGB and other parallel tasks.
    """

    # Determine selected files based on input file or process all files in data_dir
    if input_file:
        # Load list of FASTA files from the input file (CSV or XLSX)
        if input_file.endswith(".csv"):
            fasta_files_df = pd.read_csv(input_file)
        elif input_file.endswith(".xlsx"):
            fasta_files_df = pd.read_excel(input_file)
        else:
            print("[ERROR] Unsupported file format. Please use CSV or XLSX.")
            sys.exit(1)

        # Validate FASTA column in input file
        if 'fasta_files' not in fasta_files_df.columns:
            print("[ERROR] Missing 'fasta_files' column in input file.")
            sys.exit(1)

        # List of selected FASTA files from the input file
        fasta_files = fasta_files_df['fasta_files'].tolist()
        print(f"[INFO] Processing selected files from {input_file}")
    else:
        # Use all FASTA files in data_dir if no input file is provided
        fasta_files = [f for f in os.listdir(data_dir) if f.endswith('.fasta')]
        print(f"[INFO] No input file specified. Processing all FASTA files in {data_dir}: {fasta_files}")

    # Step 1: Run prepare_and_mash_input.py inside Docker with selected files
    print("[STEP 1/5] Running FASTA preparation and mash input...")
    prepare_command = [
        "docker", "run", "--rm", "-v", f"{os.path.abspath(data_dir)}:/data",
        "rakanhaib/opggb", "python", "/prepare_and_mash_input.py", "/data"
    ] + fasta_files  # Append selected files as arguments
    subprocess.run(prepare_command, check=True)
    print("[INFO] FASTA preparation and mash input completed.")

    # Step 2: Run RepeatMasker on the downsampled FASTA file
    print("[STEP 2/5] Running RepeatMasker on downsampled FASTA...")
    repeatmask_command = [
    "docker", "run", "--rm", "-v", f"{os.path.abspath(data_dir)}:/data",
    "pegi3s/repeat_masker", "bash", "-c",
    f"RepeatMasker -species viridiplantae -s /data/downsampled_panSN_output.fasta -pa {threads} -no_is"]
    subprocess.run(repeatmask_command, check=True)
    print("[INFO] RepeatMasker analysis completed.")

    # Step 3: Run run_repeatmask.py inside Docker to extract the longest TR and update params.yaml
    print("[STEP 3/5] Extracting longest tandem repeat and updating parameters...")
    extract_command = [
        "docker", "run", "--rm", "-v", f"{os.path.abspath(data_dir)}:/data",
        "rakanhaib/opggb", "python", "/run_repeatmask.py"
    ]
    subprocess.run(extract_command, check=True)
    print("[INFO] Longest tandem repeat extraction completed and params.yaml updated.")

    # Step 4: Run run_pggb.py inside Docker using the specified number of threads
    print(f"[STEP 4/5] Running PGGB with {threads} threads...")
    pggb_command = [
        "docker", "run", "--rm", "-v", f"{os.path.abspath(data_dir)}:/data",
        "rakanhaib/opggb", "python", "/run_pggb.py", str(threads)
    ]
    subprocess.run(pggb_command, check=True)
    print("[INFO] PGGB alignment and graph generation completed.")

    # Step 5: Run run_stats.py inside Docker for statistical analysis
    print("[STEP 5/5] Performing statistical analysis on generated graph and alignments...")
    stats_command = [
        "docker", "run", "--rm", "-v", f"{os.path.abspath(data_dir)}:/data",
        "rakanhaib/opggb", "python", "/run_stats.py", "{}".format(threads)
    ]
    subprocess.run(stats_command, check=True)
    print("[INFO] Statistical analysis completed.")

    print("\n🎉 [WORKFLOW COMPLETE] All steps finished successfully. Results are in the specified output directory. 🎉")

if __name__ == "__main__":
    if (len(sys.argv) == 2 and sys.argv[1] == "-h") or (len(sys.argv) == 1):
        print_help()
        sys.exit(1)

    data_dir = sys.argv[1]
    input_file = sys.argv[2] if len(sys.argv) > 2 else None
    threads = int(sys.argv[3]) if len(sys.argv) > 3 else 16

    print(f"\n🚀 [WORKFLOW START] Starting workflow with data directory: {data_dir} 🚀")
    if input_file:
        print(f"[INFO] Using file list from: {input_file}")
    print(f"[INFO] Running with {threads} threads.\n")
    
    run_workflow(data_dir, input_file, threads)
