#!/bin/bash
# setup_env_aspire2a.sh
#
# Builds the mlip-mace environment on ASPIRE2A scratch, once.
# It follows the "MACE install recipe" of the mliprun repository (docs/install/mace.md),
# the same recipe that module 00 follows on a laptop. That recipe prefers conda on HPC; this
# script uses a venv to match module 00. The recipe's header reads "Last verified: pending
# first-run validation".
#
# This script was NOT executed on ASPIRE2A for your account. Lines marked CONFIRM contain a
# value or a behaviour that you must check on your first login together with your supervisor.
#
# WHERE IT RUNS: on the LOGIN node. The script only downloads and installs; it contains no
# calculation. It is the group's understanding that compute nodes have no internet access, so
# a job could not run it (confirm on first login). That installing packages on the login node
# is allowed is also to confirm with NSCC's login-node rules: a pip install is a download,
# not a calculation. The check "mlip doctor" is NOT in this script, because its CUDA line and
# library check only mean something on a compute node; module 11, section 6, runs it in an
# interactive job afterwards.
#
# How to run it (module 11, section 6):
#   1. Log in. Stay on the login node.
#   2. Load the Python module:  module load <the module you found with "module avail python">
#   3. Run:  bash ~/onboarding_scripts/setup_env_aspire2a.sh
#
# The script stops at the first error (set -e). If it stops, read the last lines it printed,
# fix the cause, and run it again: the venv, the clone and the cache symlink are not made
# twice, and pip installs only what is missing.

set -e

# --- 0. Refuse to run inside a job -------------------------------------------------------
# PBS sets the variable PBS_JOBID inside every job, interactive jobs included. Compute nodes
# most likely have no internet, so the downloads below would fail there.
# CONFIRM: the compute nodes have no internet. If you are on the login node and this check
# stops you, tell your supervisor.
if [ -n "$PBS_JOBID" ]; then
    echo "STOP: run this script on the login node, not inside a job."
    echo "Type exit to leave the job, then run this script again."
    exit 1
fi

# --- 0b. Check the internet connection before any work ----------------------------------
# pip, git clone and the model download all need it. A login node without internet fails here,
# at once, with a clear message. (The command is inside "if", so set -e does not end the
# script before the message is printed.)
if ! command -v curl > /dev/null; then
    echo "STOP: the command curl is not available on this node, so the internet check cannot run."
    echo "Tell your supervisor."
    exit 1
fi
if ! curl -sI --max-time 20 https://pypi.org > /dev/null; then
    echo "STOP: no internet connection from the login node. Tell your supervisor."
    exit 1
fi

# --- 1. Paths used below ---------------------------------------------------------------
# ~/scratch is a symlink to your folder under /scratch/users/ (module 11, section 4).
# CONFIRM: the symlink exists on your account; if it does not, make it first (section 4).
SCRATCH=$HOME/scratch
VENV=$SCRATCH/venv/mlip-mace           # the venv; module 00 uses the same name on a laptop
MLIPRUN=$SCRATCH/mliprun               # the downloaded mliprun code; keep this folder in place
if [ ! -d "$SCRATCH" ]; then
    echo "STOP: $SCRATCH does not exist. Make the symlink of module 11, section 4, first."
    exit 1
fi

# --- 2. Check the Python module ---------------------------------------------------------
# The Python module is loaded by hand before this script (see the header).
# 3.11 or 3.12 are the versions module 00 allows.
# CONFIRM: the module name on ASPIRE2A, from "module avail python".
PYV=$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')
case "$PYV" in
    3.11|3.12) echo "Python $PYV found" ;;
    *)
        echo "STOP: python3 is version $PYV, not 3.11 or 3.12."
        echo "Run 'module avail python', load a 3.11 module, and run this script again."
        exit 1
        ;;
esac

# --- 3. Send the caches to scratch -----------------------------------------------------
# pip and other tools write large caches. Your home folder has a 50 GB quota that you
# cannot see with df or quota (module 11, section 4), so the caches go to scratch.
mkdir -p "$SCRATCH/.cache" "$SCRATCH/venv"
export XDG_CACHE_HOME=$SCRATCH/.cache
# The MACE loader writes the model weights to $XDG_CACHE_HOME/mace, but mliprun's download of
# the mace-mh-* models writes to ~/.cache/mace whatever XDG_CACHE_HOME says. A symlink from
# ~/.cache to scratch covers both.
if [ -L "$HOME/.cache" ]; then
    echo "~/.cache is already a symlink"
elif [ ! -e "$HOME/.cache" ]; then
    ln -s "$SCRATCH/.cache" "$HOME/.cache"
    echo "made the symlink ~/.cache -> $SCRATCH/.cache"
elif [ -z "$(ls -A "$HOME/.cache")" ]; then
    rmdir "$HOME/.cache"
    ln -s "$SCRATCH/.cache" "$HOME/.cache"
    echo "replaced the empty ~/.cache by a symlink to $SCRATCH/.cache"
else
    echo "WARNING: ~/.cache already holds files, so it was left alone."
    echo "Downloads of the mace-mh-* models, and any run started without XDG_CACHE_HOME set,"
    echo "will write to your home folder, which has a 50 GB quota. Tell your supervisor."
fi

# --- 4. Create and activate the venv ---------------------------------------------------
if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi
source "$VENV/bin/activate"
python -m pip install --upgrade pip

# --- 5. PyTorch ------------------------------------------------------------------------
# The line below is the CUDA 12.1 line of the mliprun MACE recipe. One venv then serves both
# the CPU job and the GPU job: a CUDA build of torch also runs on the CPU.
# CPU-only alternative from the same recipe (smaller download; the GPU job would not work):
#   pip install torch --index-url https://download.pytorch.org/whl/cpu
# CONFIRM: that CUDA 12.1 matches the GPU nodes (section 8 shows how to check).
pip install torch --index-url https://download.pytorch.org/whl/cu121

# --- 6. MACE ---------------------------------------------------------------------------
pip install mace-torch ase

# --- 7. mliprun ------------------------------------------------------------------------
# The code is downloaded to scratch and installed in "editable" mode (-e), as in module 00.
# [neb] installs the correct asetools package. Never run "pip install asetools" alone.
if [ ! -d "$MLIPRUN" ]; then
    git clone https://github.com/manuelarcer/mliprun.git "$MLIPRUN"
fi
cd "$MLIPRUN"
pip install -e ".[neb]"

# --- 8. Download the MACE-MP-0 weights once ---------------------------------------------
# This line downloads the weights (about 45 MB) and prints the path of the file. It does NOT
# load the model. It uses the same file and cache path as mace_mp, which loads the model.
# XDG_CACHE_HOME is exported in step 3, so the file goes to $HOME/scratch/.cache/mace. The
# ~/.cache symlink of step 3 is there for the mace-mh-* models and for runs started without
# XDG_CACHE_HOME. The call still imports torch.
# Jobs on compute nodes download nothing, so the weights must be here before the first job.
# The call does not check that the download is complete. If a job later fails with
# "PytorchStreamReader failed reading zip archive" or "checkpoint file is corrupted", delete
# the file in ~/scratch/.cache/mace/ whose name starts with 20231203mace128L1 and run this
# line again (module 11, section 11).
# CONFIRM with NSCC's login-node rules that this is allowed: it is a download, not a calculation.
# If this line fails with a connection error, tell your supervisor.
python -c "from mace.calculators.foundations_models import download_mace_mp_checkpoint; print(download_mace_mp_checkpoint('medium')); print('OK')"

# --- 9. Next step -----------------------------------------------------------------------
# "mlip doctor" is not run here. It reads the package versions and asks torch whether CUDA is
# available; it computes nothing. Its CUDA line and library check only mean something on the
# compute node that runs your jobs, so it is run there (module 11, section 6).
echo "Setup finished. Next: the check of module 11, section 6 (an interactive job), or the first job of section 7."
