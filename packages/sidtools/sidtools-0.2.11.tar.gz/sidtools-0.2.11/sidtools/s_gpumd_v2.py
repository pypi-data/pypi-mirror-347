import os
import shutil
import subprocess
from ase.io import read, write
from ase.db import connect
import argparse

def run_gpumd_simulations(base_dir, db_file, input_files):
    """
    Combines extracting structures from .db or .xyz file, creating folders, 
    copying input files, and executing 'sbatch run_GPUMD.sh' in each folder.

    Parameters:
    - base_dir: Base folder to hold trajectory subfolders.
    - db_file: Path to .db or .xyz file.
    - input_files: List of input files to copy into each folder.
    """
    # Extract structures and create folders with input files
    if db_file.endswith(".xyz"):
        configs = read(db_file, index=":")
    elif db_file.endswith(".db"):
        configs = [row.toatoms() for row in connect(db_file).select()]
    else:
        raise ValueError("Unsupported file type. Provide a .db or .xyz file.")

    os.makedirs(base_dir, exist_ok=True)
    for i, atoms in enumerate(configs, 1):  # Number folders as trajectory_1, trajectory_2, ...
        folder_name = os.path.join(base_dir, f"trajectory_{i}")
        os.makedirs(folder_name, exist_ok=True)
        write(os.path.join(folder_name, "model.xyz"), atoms)  # ✅ FIXED: specify atoms to write
        for file in input_files:
            shutil.copy(file, folder_name)

        # Execute sbatch for run_GPUMD.sh
        sbatch_command = ["sbatch", "run_GPUMD.sh"]
        try:
            print(f"Running sbatch in {folder_name}...")
            subprocess.run(sbatch_command, cwd=folder_name, check=True)
            print(f"Successfully submitted sbatch job in {folder_name}.")
        except subprocess.CalledProcessError as e:
            print(f"Error running sbatch in {folder_name}: {e}")
        except Exception as e:
            print(f"An error occurred in {folder_name}: {e}")

def main():
    """
    Command-line interface for the `s_gpumd` tool.
    """
    parser = argparse.ArgumentParser(
        description="Create folders from .db/.xyz, copy input files, and run GPUMD simulations."
    )
    parser.add_argument("--base", required=True, help="Base folder to hold trajectory subfolders.")
    parser.add_argument("--db", required=True, help="Path to .db or .xyz file.")
    parser.add_argument(
        "--input",
        nargs="+",
        default=["run_GPUMD.sh", "nep.txt", "run.in"],
        help="Input files to copy into each folder (default: run_GPUMD.sh nep.txt run.in)"
    )

    args = parser.parse_args()

    # Run the GPUMD simulation setup
    run_gpumd_simulations(args.base, args.db, args.input)

if __name__ == "__main__":
    main()
