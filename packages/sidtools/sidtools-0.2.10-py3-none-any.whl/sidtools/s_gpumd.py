import os
import shutil
import subprocess
from ase.io import read, write
from ase.db import connect
import argparse

def run_gpumd_simulations(base_dir, db_file, input_files, min_idx, max_idx):
    """
    Extracts structures from a .db or .xyz file, creates folders, copies input files,
    and executes 'sbatch run_GPUMD.sh' in each folder from min_idx to max_idx.

    Parameters:
    - base_dir: Base folder to hold trajectory subfolders.
    - db_file: Path to .db or .xyz file.
    - input_files: List of input files to copy into each folder.
    - min_idx: Minimum trajectory index to start sbatch submission.
    - max_idx: Maximum trajectory index to end sbatch submission.
    """
    # Extract configurations
    if db_file.endswith(".xyz"):
        configs = read(db_file, index=":")
    elif db_file.endswith(".db"):
        configs = [row.toatoms() for row in connect(db_file).select()]
    else:
        raise ValueError("Unsupported file type. Provide a .db or .xyz file.")

    total_configs = len(configs)
    os.makedirs(base_dir, exist_ok=True)

    for i, atoms in enumerate(configs, 1):  # i starts from 1
        folder_name = os.path.join(base_dir, f"trajectory_{i}")
        os.makedirs(folder_name, exist_ok=True)
        write(os.path.join(folder_name, "model.xyz"), atoms)
        for file in input_files:
            shutil.copy(file, folder_name)

    # Submit jobs only from min_idx to max_idx
    for i in range(min_idx, max_idx + 1):
        folder_name = os.path.join(base_dir, f"trajectory_{i}")
        sbatch_command = ["sbatch", "run_GPUMD.sh"]
        if os.path.exists(os.path.join(folder_name, "run_GPUMD.sh")):
            try:
                print(f"Submitting job in {folder_name}...")
                subprocess.run(sbatch_command, cwd=folder_name, check=True)
                print(f"✔️ Successfully submitted sbatch job in {folder_name}.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error running sbatch in {folder_name}: {e}")
            except Exception as e:
                print(f"❌ An unexpected error occurred in {folder_name}: {e}")
        else:
            print(f"⚠️ Skipping {folder_name}: 'run_GPUMD.sh' not found.")

def main():
    """
    Command-line interface for the `s_gpumd` tool.
    """
    parser = argparse.ArgumentParser(
        description="Create folders from .db/.xyz, copy input files, and run GPUMD simulations (selectively)."
    )
    parser.add_argument("--base", required=True, help="Base folder to hold trajectory subfolders.")
    parser.add_argument("--db", required=True, help="Path to .db or .xyz file.")
    parser.add_argument(
        "--input",
        nargs="+",
        default=["run_GPUMD.sh", "nep.txt", "run.in"],
        help="Input files to copy into each folder (default: run_GPUMD.sh nep.txt run.in)"
    )
    parser.add_argument("--min", type=int, required=True, help="Minimum trajectory index to run sbatch.")
    parser.add_argument("--max", type=int, required=True, help="Maximum trajectory index to run sbatch.")

    args = parser.parse_args()

    run_gpumd_simulations(args.base, args.db, args.input, args.min, args.max)

if __name__ == "__main__":
    main()
