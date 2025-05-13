import os
import shutil
import subprocess
from ase.io import read
from ase.db import connect

def run_gpumd_simulations():
    """
    Combines extracting structures from .db or .xyz file, creating folders, 
    copying input files, and executing 'sbatch run_GPUMD.sh' in each folder.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Create folders from .db/.xyz and copy model.xyz + GPUMD input files, then run sbatch."
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

    # Extract structures and create folders with input files
    if args.db.endswith(".xyz"):
        configs = read(args.db, index=":")
    elif args.db.endswith(".db"):
        configs = list(connect(args.db).select())
    else:
        raise ValueError("Unsupported file type. Provide a .db or .xyz file.")

    os.makedirs(args.base, exist_ok=True)
    for i, atoms in enumerate(configs, 1):  # Number folders as trajectory_1, trajectory_2, ...
        folder_name = os.path.join(args.base, f"trajectory_{i}")
        os.makedirs(folder_name, exist_ok=True)
        atoms.write(os.path.join(folder_name, "model.xyz"))
        for file in args.input:
            shutil.copy(file, folder_name)

        # Execute sbatch for run_GPUMD.sh
        sbatch_command = ["sbatch", os.path.join(folder_name, "run_GPUMD.sh")]
        try:
            print(f"Running sbatch in {folder_name}...")
            subprocess.run(sbatch_command, check=True)
            print(f"Successfully submitted sbatch job in {folder_name}.")
        except subprocess.CalledProcessError as e:
            print(f"Error running sbatch in {folder_name}: {e}")
        except Exception as e:
            print(f"An error occurred in {folder_name}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Create folders from .db/.xyz and copy model.xyz + GPUMD input files."
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
    prepare_gpumd_inputs(args.base, args.db, args.input)

if __name__ == "__main__":
    main()
