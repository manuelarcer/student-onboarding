# 00. Setup: install the tools on your own computer

- Goal: a working Python environment on your laptop with the group's `mliprun` tool, the MACE model and Jupyter, confirmed by `mlip doctor`.
- Before you start: a laptop (Windows, macOS or Linux) on which you are allowed to install software, an internet connection, and about 3 GB of free disk space.
- Time to work through it: about 2 hours, most of it waiting for downloads.
- After this you can: open a terminal and activate the environment; run `mlip doctor` and read its output; start Jupyter Lab inside this repository.
- Files: none. This module is text only. Everything you install goes into one folder, `~/mlip` (step 4).

Every step gives the command to type, then **Expected:** what you should see. If you see
something else, stop and read the troubleshooting table in step 13. Run the commands one
line at a time, and wait for each to finish before typing the next.

Commands differ between operating systems. Where they differ, each step shows three
variants: **Windows** (PowerShell), **macOS** (Terminal) and **Linux** (bash; the wording is
for Ubuntu). Use only the variant for your computer.

Only the macOS steps were executed end to end by the author (2026-09-17, macOS on
Apple Silicon, Python 3.11.10). The Windows and Linux steps come from mliprun's tested
install guides. If a Windows or Linux step fails, tell your supervisor; the text will be
corrected.

## 1. What you are installing and why

Three words this module uses everywhere:

- A **terminal** is a window where you type commands as text and the computer answers with text. On Windows the program is called PowerShell (open it from the Start menu, or inside VS Code). On macOS it is the Terminal app (Applications, then Utilities, or search "Terminal" with Spotlight). On Linux it is usually also called Terminal (Ctrl+Alt+T on Ubuntu). Everything in this course except the notebooks happens in a terminal.
- **Python** is the programming language the group's tools are written in. You do not need to know it yet; module 01 teaches what you need.
- A **package** is a piece of Python software written by someone else that you install with the command `pip`. `pip` downloads the package from the internet and puts it where Python can find it.

What you install, in the order of the steps below:

- **Python 3.11** (step 2). The language itself. Version 3.11 or 3.12; older and newer versions do not work with all the packages below.
- **git** (step 3). A program that downloads a folder of code and keeps track of its versions. Such a folder is called a **repository**. You use git to get `mliprun` and this course from GitHub, a website that stores repositories.
- A **virtual environment** (step 5), written **venv** for short. A private folder that holds one copy of Python and the packages installed for one purpose. Packages inside it do not touch the rest of your computer, and packages elsewhere do not touch it. You must **activate** the venv in every new terminal before using it; activating only changes which Python the terminal uses. The venv in this module is called `mlip-mace`.
- **PyTorch** (step 6), called `torch` in commands. The numerical library the MACE model runs on. You install the CPU version: every module in this course runs on the processor, without a graphics card.
- **MACE** (step 7), the package `mace-torch`. A machine-learning interatomic potential (MLIP): a model that predicts the energy and forces of a set of atoms much faster than density functional theory. The model you use is MACE-MP-0, trained on Materials Project data. One MLIP per venv: `mliprun` also supports other models (UMA, SevenNet, CHGNet), but their packages need different versions of `torch` and break each other when installed together. Never install another MLIP into `mlip-mace`.
- **mliprun** (step 8). The group's tool. It gives you the command `mlip`, with subcommands for geometry optimization (`mlip optimize`), molecular dynamics (`mlip md`), nudged elastic band (`mlip neb`) and an environment check (`mlip doctor`). It is installed from its GitHub repository, not from the public package index that `pip` uses by default.
- **Jupyter Lab** (step 9), together with `pymatgen` and `mp-api`. Jupyter Lab is the program that opens the notebooks of this course in your web browser. A **notebook** is a file that mixes text, code and the output of that code. A **kernel** is the Python process that runs the code of one notebook; Jupyter starts one per notebook, using the Python of your venv. `pymatgen` builds crystal structures and surfaces (module 04); `mp-api` downloads structures from the Materials Project database (module 03).

## 2. Install Python 3.11 or 3.12

If you already have Python 3.11 or 3.12, run only the check at the end of this step; on
Ubuntu, still run the `sudo apt install python3.X-venv` line of case (a) in the Linux
section, because Ubuntu does not install the venv part by default.

**Windows**

1. Go to https://www.python.org/downloads/windows/ and download the "Windows installer (64-bit)" for the latest Python 3.11.
2. Run it. On the first screen, tick the box **"Add python.exe to PATH"** at the bottom, then click "Install Now". The PATH is the list of folders where the terminal looks for programs; without that box, Python is not on the list and PowerShell does not find `python`.
3. Close PowerShell and open it again.

Check:

```powershell
python --version
```

Expected: `Python 3.11.9` or another 3.11.x or 3.12.x number. If the Microsoft Store opens
instead, the box was not ticked: run the installer again, choose "Modify", and tick it.

**macOS**

Option A, if you have Homebrew, a program that installs software on macOS from the
terminal (check with `brew --version`; if that prints `command not found`, use option B):

```bash
brew install python@3.11
```

Option B: download the "macOS 64-bit universal2 installer" for Python 3.11 from
https://www.python.org/downloads/macos/ and run it with the default choices.

Check:

```bash
python3.11 --version
```

Expected: `Python 3.11.10` or another 3.11.x number. `python3 --version` may print an
older version (3.9) that came with macOS; that is normal. This guide always calls
`python3.11` by its full name.

**Linux (Ubuntu)** (these lines were not executed by the author)

First see which Python your system already has; the version depends on your Ubuntu
release:

```bash
python3 --version
```

Then follow the one case that matches what it printed.

**Case (a):** it prints `Python 3.11.x` or `Python 3.12.x`. Install only the venv part
for that version (write `3.11` or `3.12` in place of `3.X`), and use `python3.X` in
every later command of this module:

```bash
sudo apt update && sudo apt install python3.X-venv
```

**Case (b):** it prints anything else, older or newer than 3.12. Install 3.11 from the
"deadsnakes" package source, which provides extra Python versions for Ubuntu. The
exercises are verified on 3.11 and 3.12 and on nothing newer, so do not use a newer
system Python even if you have one.

```bash
sudo apt update && sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv
```

**Case (c):** after adding the source, `apt` answers
`E: Unable to locate package python3.11`. There is no 3.11 build for your Ubuntu
release. Install Miniforge (https://github.com/conda-forge/miniforge) and follow the
"Conda recipe" in mliprun's `docs/install/mace.md` instead of the venv: conda replaces both
the venv commands of step 5 and the activation commands of step 12. Tell your
supervisor that you are on this route.

Expected (cases (a) and (b)): `sudo` asks for your password; `apt install` asks
`Do you want to continue? [Y/n]`, answer `Y`. In case (b) only, `add-apt-repository` also asks
you to press Enter.
Check with the version you installed (`3.11` or `3.12`):

```bash
python3.11 --version
```

Expected: `Python 3.11.x` (or `Python 3.12.x` from `python3.12 --version` in case (a)
with 3.12).

If you use 3.12 instead of 3.11, on any system, type `python3.12` wherever this module
says `python3.11`.

## 3. Install git

**Windows**

1. Go to https://git-scm.com/downloads and download the 64-bit installer for Windows.
2. Run it. Keep the default choices, except where this table says otherwise:

| Setup screen | Choice | Why |
|---|---|---|
| Adjusting your PATH environment | "Git from the command line and also from 3rd-party software" | Allows you to use `git` in PowerShell or the VS Code terminal |
| Choosing the default editor | "Vim" or "VS Code" (your preference) | VS Code is easier for most users |
| Configuring line endings | "Checkout Windows-style, commit Unix-style line endings" | Recommended default for Windows |
| Other options | Leave as default | Safe for most users |

3. Close PowerShell and open it again.

**macOS**

```bash
xcode-select --install
```

Expected: a window asks whether to install the "command line developer tools"; click
Install and wait (5 to 20 minutes). If the terminal prints
`xcode-select: note: Command line tools are already installed`, you already have git.

**Linux (Ubuntu)**

```bash
sudo apt update && sudo apt install git
```

Check (all systems):

```
git --version
```

Expected: `git version 2.47.0` or another 2.x number (on Windows it ends with
`.windows.1`).

## 4. Make a working folder

This folder will hold the venv, the `mliprun` code and this course.

**macOS and Linux**

```bash
mkdir ~/mlip && cd ~/mlip
```

**Windows**

```powershell
mkdir $HOME\mlip; cd $HOME\mlip
```

Expected: on macOS and Linux, no output; on Windows, a short table describing the new
folder. `~` and `$HOME` both mean your home folder. If `mkdir` says the folder already
exists, that is fine: run only the `cd` part.

## 5. Create and activate the virtual environment

**macOS and Linux**

```bash
python3.11 -m venv mlip-mace
source mlip-mace/bin/activate
```

**Windows**

```powershell
python -m venv mlip-mace
.\mlip-mace\Scripts\activate
```

If PowerShell refuses the second line with a message that ends in
`running scripts is disabled on this system`, run this once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Answer `Y`, then repeat the activate line.

Expected: the first command prints nothing and takes a few seconds; a folder `mlip-mace`
appears. After the second command, the prompt (the text the terminal prints before the
cursor, where you type) starts with `(mlip-mace)`. That prefix means the venv is active.
It disappears when you close the terminal; step 12 shows how to get it back.

Now update `pip` inside the venv (all systems):

```
python -m pip install --upgrade pip
```

Expected: ends with `Successfully installed pip-26.2.1` or a newer number, or says
`Requirement already satisfied`.

From here to step 10, every command needs the `(mlip-mace)` prefix in the prompt. If it
is missing, activate again first.

## 6. Install PyTorch (CPU version)

Same command on all systems:

```
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

Expected: a download of about 130 MB on macOS (more on Windows and Linux), then a line
`Successfully installed ...` that contains `torch-2.` followed by a version number.

## 7. Install MACE

Same command on all systems:

```
pip install mace-torch
```

Expected: several minutes and many packages; the last line is
`Successfully installed ...` and contains `mace-torch-0.3.` followed by a version
number.

## 8. Download and install mliprun

Same commands on all systems, one line at a time:

```
git clone https://github.com/manuelarcer/mliprun.git
cd mliprun
pip install -e ".[neb]"
cd ..
```

Expected: `git clone` prints `Cloning into 'mliprun'...` and a few progress lines, and a
folder `mliprun` appears. `pip install` ends with `Successfully installed ...` containing
`mliprun-0.4.0` (or newer) and `asetools`. The `-e` means "editable": Python reads the
code from the `mliprun` folder you just downloaded, so keep that folder where it is.
`[neb]` adds the helper package `asetools`, downloaded from GitHub.

> **Warning.** Never run `pip install asetools`. The package with that name on the public
> index is an unrelated program (a tool for a pixel-art editor) and it hides the real
> one. The `[neb]` extra above installs the correct `asetools` from GitHub. If you already
> ran the wrong command: `pip uninstall asetools`, then run `pip install -e ".[neb]"`
> again inside the `mliprun` folder.

## 9. Install the notebook tools

Same command on all systems:

```
pip install jupyterlab pymatgen mp-api
```

Expected: a few minutes; the last line `Successfully installed ...` contains `jupyterlab-`,
`pymatgen-` and `mp-api-` with version numbers.

## 10. Verify

First the environment check:

```
mlip doctor
```

Expected (your version numbers may be newer; on Windows the first line says `win32`, on
Linux `linux`):

```
mliprun environment doctor
================================
Python          3.11.10 (darwin)
mliprun         0.4.0
ase             3.29.0
asetools        OK (real package; NEB sanity checks active)
torch           2.14.0
CUDA            not available (CPU only)

MLIP packages (one env per MLIP — see ADR 0001):
  fairchem-core  not installed
  mace-torch     0.3.16
  sevenn         not installed
  chgnet         not installed

(one line naming the default model; ignore it, this course always names the model)

Environment OK.
```

The three lines that matter: `mace-torch` shows a version number, `CUDA` says
`not available (CPU only)`, and the last line is `Environment OK.`. If the last line is
`Environment NOT usable`, step 7 did not finish: repeat it and read its last 20 lines.

Then load the model once (same command on all systems, one long line):

```
python -c "from mace.calculators import mace_mp; mace_mp(model='medium', device='cpu'); print('OK')"
```

Expected: the first time, a line `Downloading MACE model from 'https://github.com/...'`
and a progress line that reaches `100.0% (42.4 MB / 42.4 MB)`; the file (the MACE-MP-0
model weights, about 45 MB; the progress line counts in units of 1024 x 1024 bytes (MiB) and prints them as `MB`, so it shows 42.4) is saved in `~/.cache/mace/` (Windows:
`C:\Users\<your name>\.cache\mace\`). Then several warning lines (`FutureWarning`,
`UserWarning`, `WARNING:root:Default dtype float32 ...`), which you can ignore, a few
lines starting with `Using`, and `OK` as the last line. This takes about one minute. The
second time there is no download. If the last line is not `OK`, see step 13.

## 11. Get this course and open it

Still inside `~/mlip` with the venv active.

```
git clone https://github.com/manuelarcer/student-onboarding.git
cd student-onboarding
jupyter lab
```

Expected: a browser tab opens with Jupyter Lab; the file browser on the left shows
`modules/`, `paths/` and `projects/`. The terminal keeps printing messages; leave it
open while you work. If no tab opens, copy the address that starts with
`http://localhost:8888/lab?token=` from the terminal into your browser.

To stop Jupyter Lab: go to the terminal, press Ctrl+C, and answer `y`.

## 12. Every day

Open a terminal, then:

**macOS and Linux**

```bash
cd ~/mlip
source mlip-mace/bin/activate
cd student-onboarding
jupyter lab
```

**Windows**

```powershell
cd $HOME\mlip
.\mlip-mace\Scripts\activate
cd student-onboarding
jupyter lab
```

Expected: `(mlip-mace)` in the prompt after the second line, and a browser tab after the
last one. When you finish: Ctrl+C in the terminal stops Jupyter; `deactivate` leaves
the venv, or simply close the terminal.

## 13. Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| `zsh: command not found: mlip` (macOS), `bash: mlip: command not found` (Linux) or `The term 'mlip' is not recognized` (Windows) | The venv is not active in this terminal | Run the activate line from step 12 and check that the prompt shows `(mlip-mace)` |
| `error: externally-managed-environment` | You ran `pip install` outside the venv, into the system Python | Activate the venv (step 12) and repeat the command. Never add `--break-system-packages` |
| `... cannot be loaded because running scripts is disabled on this system` (Windows) | PowerShell blocks the activate script by default | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once, then repeat the activate line |
| A download stops making progress, or fails with `ReadTimeoutError` or `Connection reset` | Slow or interrupted connection; `torch` is 130 MB or more and the MACE weights 45 MB | Press Ctrl+C and repeat the same command; `pip` continues from what it already saved. On a campus network, try again later or from another network |
| The model command (step 10) ends with `PytorchStreamReader failed reading zip archive` or `checkpoint file is corrupted` | The weights download stopped early and left an incomplete file; MACE does not notice | Delete the file in `~/.cache/mace/` whose name starts with `20231203mace128L1` (Windows: `C:\Users\<your name>\.cache\mace\`), then repeat the model command |
| The Microsoft Store opens when you type `python` (Windows) | Python is not on the PATH | Run the python.org installer again, choose "Modify", tick "Add python.exe to PATH", then open a new PowerShell |
| `zsh: command not found: python3.11` (macOS) or `bash: python3.11: command not found` (Linux) | Step 2 was skipped or installed another version | Run step 2 again; if you installed 3.12, type `python3.12` |
| `E: Unable to locate package python3.11` (Ubuntu) | Your Ubuntu release has no `python3.11` package; which Python is available depends on the release | Follow the Linux part of step 2: case (a) if `python3 --version` prints 3.11 or 3.12; case (b) adds the deadsnakes source; case (c) Miniforge if the message appears even after adding the source |
| `python3.X -m venv` fails with `ensurepip is not available` (Ubuntu) | The venv part of Python is a separate package on Ubuntu and is not installed | `sudo apt update && sudo apt install python3.X-venv` with your version (3.11 or 3.12) in place of `3.X`, then repeat the venv command of step 5 |
| `mlip doctor` prints `asetools WARN: wrong package` | `pip install asetools` was run at some point | `pip uninstall asetools`, then `pip install -e ".[neb]"` inside the `mliprun` folder |
