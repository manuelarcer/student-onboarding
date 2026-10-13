# 11. ASPIRE2A: run the same calculation on a supercomputer

- Goal: log in to the ASPIRE2A supercomputer, build the `mlip-mace` environment there, and run a geometry optimization with `mliprun` as a job, first on CPU cores and then on a GPU.
- This module is optional. Most of the work of this course runs on your own computer. Do this module only if you get a free personal ASPIRE2A account (section 2); if you do not, skip it.
- Before you start: modules 00 to 10 finished; a free personal ASPIRE2A account (section 2); the `mlip-mace` environment of module 00 on your laptop; a `POSCAR` file from an earlier module to use as the test structure.
- Time to work through it: about 3 hours, plus the first login, which you do together with your supervisor. This is an estimate; the author has not timed it on ASPIRE2A.
- After this you can: log in and move files between your laptop and ASPIRE2A; say what you may and may not run on the login node; install the environment on the login node and check it in a job; submit, watch and cancel a job with `qsub`, `qstat` and `qdel`; say which settings of a job a supervisor decides.
- Files: `job_cpu.pbs`, `job_gpu.pbs`, `setup_env_aspire2a.sh`. This module has no notebook.

**Status of this module.** It was written from the group's experience with ASPIRE2A. It was
not executed for your account: the author cannot log in as you. Confirm each step with your
supervisor on your first login. Some values are marked "confirm" on purpose, because only
your account can show them: the login host name (check the welcome email), the name of the
Python module (section 6) and the charging code to use (sections 2 and 10). A statement about ASPIRE2A
that comes from the group's experience, or that nobody checked, is labelled as such: "from
the group's experience" or "confirm on first login".

Expected blocks in this module describe what the group has seen on ASPIRE2A in the past.
The exact wording on your screen may differ. If something differs in a way that matters, stop
and ask your supervisor.

This module uses the terminal skills of module 00. On Windows, use PowerShell; on macOS and
Linux, use Terminal. Commands typed on ASPIRE2A are marked **on ASPIRE2A**; commands typed
on your laptop are marked **on your laptop**.

## 1. What ASPIRE2A is

- **ASPIRE2A** is a supercomputer run by the National Supercomputing Centre (NSCC) in Singapore. It is many computers, called **nodes**, connected by a fast network and used by many people at the same time.
- You do not run programs on it by clicking. You log in with a terminal and type commands, as in module 00.
- There are two kinds of node you care about:
    - The **login node** is the computer you reach when you log in. Every user of ASPIRE2A shares it. It is for light work: looking at files, editing text, and giving orders to the scheduler.
    - A **compute node** is a computer that does the heavy work. You cannot log in to one directly. You ask for one, and the scheduler gives you one for a limited time.
- The **scheduler** is the program that decides which job runs where and when. ASPIRE2A uses **PBS**. You give PBS a **job**: a request for resources (how many CPU cores, how much memory, whether a GPU, for how long) together with the commands to run.
- A **job script** is the text file that holds both parts. The lines that start with `#PBS` are the request; the other lines are ordinary shell commands, the same ones you would type at a terminal. You submit the file with `qsub`.
- A **queue** is a waiting line that PBS keeps. Your job waits in a queue until the resources it asked for are free. The job script names the queue. The only queue this module uses is `normal`.
- The **walltime** is the longest time the job may run, measured by a clock on the wall, not by CPU time. If the job is still running when the walltime ends, PBS stops it and the results that were not yet saved are lost. A small walltime also helps your job start earlier, because PBS can fit it into a gap.
- A **GPU** is a graphics card used as a fast numerical processor. Section 8 explains when it is worth asking for one.

## 2. Get access

1. You apply for a free personal NSCC ASPIRE2A account. Your supervisor will point you to the application page; this module does not give an address or steps, because they may change. According to the group, this kind of account comes with 100,000 CPU hours. Confirm the current allocation in the NSCC welcome email or on the NSCC website.
2. You will most likely not be added to the group's ASPIRE2A projects. The account is yours, and so are its CPU hours (section 10).
3. VASP is not available to you on this account. The account is for MLIP jobs with the tools of this course.
4. NSCC sends you a welcome email with your **username** and the way to set your password. Follow that email; this module does not repeat it because the steps may change.
5. The email also gives the address of the login node. The group has used `aspire2a.nscc.sg`. Check the welcome email; if it says something different, use the address in the email wherever this module writes `aspire2a.nscc.sg`.
6. Find the **charging code** to write in your job scripts (section 10). Your supervisor will show you where the code of your free account is shown, for example in the NSCC welcome email; confirm this. You do not need the code to log in, but you need it before you submit any job. Confirm it with your supervisor before your first job.
7. Ask your supervisor whether you must be on the A*STAR network or a VPN to reach ASPIRE2A from where you work. The group has not recorded this for students. Confirm on first login.

## 3. Log in

**On your laptop**, open a terminal. macOS and Linux include the `ssh` command, and so does PowerShell on Windows, so you install nothing. `ssh` opens a terminal session on another computer over the network. Write your username in place of `<username>`, with no angle brackets:

```
ssh <username>@aspire2a.nscc.sg
```

The first time you connect to any computer, `ssh` shows its fingerprint (a short code that identifies the computer) and asks whether to trust it:

```
The authenticity of host 'aspire2a.nscc.sg (...)' can't be established.
...
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Type `yes` and press Enter. Then type your password and press Enter. The terminal shows
nothing while you type the password; no dots, no stars. That is normal.

Expected: some welcome text, then a prompt that contains your username and the name of the
login node. Every command from here on, until you type `exit`, runs on ASPIRE2A. Check
where you are:

```
pwd
```

Expected: a path that starts with `/home/users/` (from the group's experience; confirm on first login). This is your **home folder**. Then:

```
myquota
```

Expected: a table of your disk space, used and allowed, for your home folder and for scratch
(section 4). `myquota` is a command of ASPIRE2A, not of your laptop. The layout of its
output is not recorded here; ask your supervisor to read it with you the first time.

To leave ASPIRE2A, type `exit`. The prompt returns to your laptop.

If you see `Permission denied, please try again.`, the username or the password is wrong;
after three tries `ssh` stops. If the connection hangs and then says `Connection timed out`, see
the table in section 11.

## 4. Where files go

ASPIRE2A has two places for your files, and they are not equal:

| Place | Path | Size | Use it for |
|---|---|---|---|
| Home folder | `/home/users/...` (`~` for short) | **50 GB quota** | Scripts and small text files only |
| Scratch | `/scratch/users/...` | Much larger; `myquota` shows yours | Calculations, the venv, caches, model weights |

- A **quota** is the maximum amount of disk space you may use.
- From the group's experience, the 50 GB quota of the home folder is hidden from the usual tools. `df` and `quota` do not show it; only `myquota` does. A home folder that is full does not give a clear message: copying files with `rsync` can fail with `unexpected end of file` while `ssh` still works. When something odd happens with files, run `myquota` first.
- **Scratch** is working space for large files. Confirm on first login whether files in scratch are deleted after some time without use; ask your supervisor before you keep anything there that you cannot recreate.
- A **symlink** (symbolic link) is a name that points to another folder, like a shortcut. On ASPIRE2A, `~/scratch` is normally a symlink to your folder under `/scratch/users/`. The exact path depends on your institute and username and is not written here. **On ASPIRE2A**, check whether the symlink exists:

```
ls -ld ~/scratch
```

Expected, if it exists: a line that contains `scratch -> /scratch/users/...`. The part after `->` is your scratch folder. If it says `No such file or directory`, look for your folder with `ls /scratch/users/`, step down one folder at a time (`ls /scratch/users/<next name>`) until you find a folder with your username, and make the symlink yourself (write the full path you found in place of `<your scratch folder>`):

```
ln -s <your scratch folder> ~/scratch
```

Now make the folders this module uses:

```
mkdir -p ~/scratch/onboarding ~/onboarding_scripts
cd ~/scratch
pwd
```

Expected: `pwd` prints a path that starts with `/scratch/users/`. The folder `~/onboarding_scripts`
is in your home folder, which is correct because it will hold three small text files.

## 5. Rules for the login node

The login node is shared by every user, so one heavy command slows it down for everybody.
From the group's experience, the system blocks an account automatically when it detects
heavy work on the login node, and an account of the group was blocked for this.
Confirm with your supervisor what a blocked account can and cannot do.

**Never run on the login node:**

- `du` (it reads the size of every file in a folder) or `find` over large folders
- Python analysis, a notebook, or any calculation, `mlip optimize`, `mlip md` and `mlip neb` included
- `mlip doctor`: it computes nothing, but its CUDA line and library check only mean something on the compute node that runs your jobs, so it runs in a job (section 6)

**Fine on the login node:**

- `ls`, `cat`, `pwd`, `cd`, `mkdir`
- `qsub`, `qstat`, `qdel` (section 7) and `myquota`
- editing a text file with a terminal editor; confirm on first login which editors are installed (`nano` is the easiest)
- a short `rsync` or `scp` (section 9) of a few files
- **Downloads and package installation**, which is the exception this module relies on: `pip install`, `git clone` and the download of model weights, as the setup of section 6 does. A `pip install` is a download, not a calculation. Compute nodes most likely have no internet (the group's understanding; confirm on first login), so the login node is the only place where downloads can happen. Confirm with NSCC's login-node rules that installing packages there is allowed. Calculations and heavy analysis are not allowed there, and the setup of section 6 contains none.

When you are unsure whether a command is heavy, ask your supervisor before you run it.

## 6. Set up the environment once

You build the same `mlip-mace` environment as in module 00, on scratch, with a script that
runs on the login node (see below why). The recipe is the
group's MACE install recipe (`docs/install/mace.md` in the `mliprun` repository), as in
module 00. That recipe prefers conda on HPC; this module uses a venv, to match module 00, and does not use conda. The recipe's own header reads "Last verified: pending first-run validation", so treat it as unvalidated on ASPIRE2A. Two lines of the script are the ones you would otherwise type by hand:

- `pip install torch --index-url https://download.pytorch.org/whl/cu121` installs PyTorch built for CUDA 12.1, the version the recipe names for GPU nodes of an HPC system. The same recipe gives `https://download.pytorch.org/whl/cpu` for a CPU-only install, and says nothing more specific about ASPIRE2A. A CUDA build of PyTorch also runs on the CPU, so this one venv serves both jobs (sections 7 and 8). Confirm CUDA 12.1 against the GPU nodes with `mlip doctor` in section 8.
- `pip install mace-torch ase` installs MACE, as in module 00 step 7.

Everything else in the script does what module 00 did, with these differences:

- The venv lives in `~/scratch/venv/mlip-mace`, and the `mliprun` code in `~/scratch/mliprun`. Keep that folder in place: the `-e` of `pip install -e` means the venv reads the code from it.
- `XDG_CACHE_HOME` is a setting that many programs, `pip` included, use as the folder for their caches. The script points it to `~/scratch/.cache`. The two places that save MACE weights behave differently. The MACE loader that serves `--mlip mace` reads `XDG_CACHE_HOME` and writes to `$XDG_CACHE_HOME/mace` (function `get_cache_dir` in `mace/tools/utils.py` of the `mace-torch` version used to check this module; the weights of `--mlip mace` are loaded by `mace_mp()` in `mace/calculators/foundations_models.py`). The `mliprun` code that downloads the `mace-mh-*` models writes to `~/.cache/mace` whatever `XDG_CACHE_HOME` says (function `_ensure_mace_foundation_checkpoint`, file `src/mliprun/cli/utils.py`). So the script also makes `~/.cache` a symlink to `~/scratch/.cache`, if `~/.cache` does not exist or is empty, to cover both.
- The script downloads the MACE-MP-0 weights with `download_mace_mp_checkpoint('medium')` of MACE, which saves the same file in the same cache folder that the model loader of module 00 uses. It downloads the weights and does not load the model; it still imports `torch`, so it takes a few seconds. It is a download, not a calculation; confirm this with NSCC's login-node rules. It does not check that the download is complete (section 11 has the row for a truncated file). `mlip doctor`, the other check of module 00, runs in a job (below).

**On your laptop**, copy the three files of this module to ASPIRE2A. `scp` copies files over `ssh`. Go to this module's folder first (the path is the one from module 00; on Windows, replace `/` with `\`):

```
cd ~/mlip/student-onboarding/modules/11-hpc-aspire2a
scp setup_env_aspire2a.sh job_cpu.pbs job_gpu.pbs <username>@aspire2a.nscc.sg:onboarding_scripts/
```

Expected: one line per file, each with a percentage that reaches `100%`, and its size. The
remote path `onboarding_scripts/` is relative to your home folder on ASPIRE2A (section 4
made it).

If you copied the files from a Windows computer, they may have Windows line endings, which break shell scripts (section 11). **On ASPIRE2A**, remove the extra character from the three files right after copying; it does no harm if they were already fine:

```
cd ~/onboarding_scripts
sed -i 's/\r$//' setup_env_aspire2a.sh job_cpu.pbs job_gpu.pbs
```

**The setup runs on the login node, not in a job.** The setup downloads packages, code and
model weights from the internet. It is the group's understanding that the compute nodes of
ASPIRE2A have no internet access; confirm this on first login. If so, a job could not run the
setup, and every download must happen on the login node. Installing packages on the login node
is also something to confirm with NSCC's login-node rules: a `pip install` is a download, not a
calculation, and section 5 treats it that way, but NSCC's rules decide. The setup script
checks that the login node can reach the internet before it starts. What does run in a job is
the check at the end of this section, because its result only means something on the compute
node that runs your jobs.

In the same way, the jobs of sections 7 and 8 download nothing: the model weights must already
be in your cache when the job starts. If you later use another model, download its weights on
the login node first.

On the login node, find the Python module. A **module** is ASPIRE2A's way to make an
installed program available: `module load <name>` adds it to your terminal session. (This
only lists and loads a program; it is light enough for the login node.)

```
module avail python
```

Expected: a list of modules whose names contain `python`. You need one that is Python 3.11
or 3.12 (module 00, step 2 gives the reason). **The exact name is not written here;
confirm it from this list.** Load it, writing its name in place of `<python module>`, and check:

```
module load <python module>
python3 --version
```

Expected: `Python 3.11.x` or `Python 3.12.x`. Write down the module name; section 7 may need it.

Now run the script, still on the login node. `bash` runs the file as a script; you do not need to make it executable:

```
bash ~/onboarding_scripts/setup_env_aspire2a.sh
```

Expected: the script stops at once with `STOP:` if you started it inside a job
(`STOP: run this script on the login node, not inside a job`), if the login node cannot
reach the internet (`STOP: no internet connection from the login node`), if `curl` is
missing, if `~/scratch` does not exist (the line reads `STOP: $SCRATCH does not exist. Make the symlink of module 11, section 4, first.`, with `$SCRATCH` printed as your home folder path followed by `/scratch`), or if the Python version is wrong. Otherwise it prints a short line about the Python version and one about the cache symlink, then the long output of
`pip install` (the CUDA build of `torch` is a much larger download than the 130 MB CPU
build of module 00 on macOS, so allow time), then the path of the downloaded weights file and the line `OK`, and a last line:
`Setup finished. Next: the check of module 11, section 6 (an interactive job), or the first job of section 7.`
The script does not run `mlip doctor`. `mlip doctor` computes nothing; it reads the package
versions and asks `torch` whether CUDA is available. Its CUDA line and library check only mean
something on the compute node that runs your jobs, so it runs in a job.

If the script stops with `STOP: no internet connection from the login node`, or later with a
connection error in the `pip`, `git clone` or model step, do not work around it by yourself;
tell your supervisor. If it stops for another reason, fix the cause and run it again: the venv, the
clone of `mliprun` and the cache symlink are not made twice, and `pip` only installs what is
missing.

**Check the environment in a job.** An **interactive job** is a job that gives you a terminal
on a compute node, for a limited time, instead of running a script. Write the charging code
shown for your free account (section 2) in place of `PROJECT_CODE`; CPU hours of this check count
against your free allocation, so keep the walltime short:

```
qsub -I -P PROJECT_CODE -l select=1:ncpus=8:mem=32gb -l walltime=00:30:00 -q normal
```

The flags: `-I` means interactive; `-P` is the charging code; `select=1:ncpus=8:mem=32gb`
asks for one node with 8 CPU cores and 32 GB of memory; `walltime=00:30:00` is 30 minutes;
`-q normal` names the queue.

Expected: a line saying that the job is waiting to start, then, when resources are free, a
line saying that the job is ready and a new prompt that shows the name of a compute node
instead of the login node. The wait can be seconds or hours. If the wait is long, leave
the terminal open. In the job, load the Python module again (a job starts a new session), activate the venv and run the check:

```
module load <python module>
source ~/scratch/venv/mlip-mace/bin/activate
mlip doctor
```

Expected: a report like the one in module 00, step 10. `mace-torch` shows a version number and the last
line is `Environment OK.`. The `CUDA` line says `not available (CPU only)` here, because this
job has no GPU: that is correct. Section 8 shows the same line on a GPU node. Type `exit` once to end the interactive job and return to the login node. If the job reaches its
walltime first, PBS ends it for you.

The first job of section 7 is the second check: if the interactive job is not convenient, you can skip it and go to section 7, where `mlip` runs for the first time on a compute node.

## 7. Your first job

You run a geometry optimization of the structure you give it, as in module 07, now as a job.

1. **On ASPIRE2A**, make a run folder in scratch and copy the job script into it:

    ```
    mkdir -p ~/scratch/onboarding/first_job
    cp ~/onboarding_scripts/job_cpu.pbs ~/scratch/onboarding/first_job/
    ```

2. **On your laptop**, copy a `POSCAR` to that folder. Use a small structure from an
   earlier module. A file called `POSCAR` is expected: the job script names it. Replace `<path to your POSCAR>` with its path:

    ```
    scp <path to your POSCAR> <username>@aspire2a.nscc.sg:scratch/onboarding/first_job/POSCAR
    ```

3. **On ASPIRE2A**, open the script and read it completely before you submit anything:

    ```
    cd ~/scratch/onboarding/first_job
    cat job_cpu.pbs
    ```

   The lines that start with `#PBS` are the request. In order: the job name (`-N`); one node
   with 16 CPU cores and 64 GB of memory (`-l select=...`); the walltime of 1 hour (`-l walltime`);
   `-j oe`, which joins the error messages and the normal messages into one output file; the charging code
   (`-P`); and the queue (`-q`). The lines after them are the commands: go to the folder
   where you ran `qsub` (`$PBS_O_WORKDIR`), set the number of threads, point the caches to scratch, and run `mlip optimize run`
   with the model named (`--mlip mace`) and the device named (`--device cpu`).

4. Open the file with `nano job_cpu.pbs` and check three lines, each found by its content and each with a comment that starts with `EDIT` above it:
    - the line that starts with `#PBS -N`: the job name. Write a short name of your choice. `qstat` may show a long name cut short; the PBS version of ASPIRE2A was not confirmed, so no limit is stated here
    - the line that starts with `#PBS -P`: replace `PROJECT_CODE` with the charging code of your free account (section 2); confirm it with your supervisor before the first job
    - the line that starts with `MLIP=`: the path of the venv. Leave it as it is if you followed section 6

   Two more things in the file. The comment line `# module load <python module>` is switched off by its `#`. Remove the `#` and write the module name from section 6 only if the job fails with a message about a missing Python library or shared library (section 11). And save the file with `nano`: Ctrl+O then Enter saves, and Ctrl+X leaves.
5. Submit it:

    ```
    qsub job_cpu.pbs
    ```

   Expected: one line, a **job ID** that starts with a number, such as `1234567.something` (the format after the number is from the group's experience; confirm on first login). The number is the
   important part. If PBS refuses the job, the message says why; the most common reason
   is a wrong or missing charging code (section 11).

6. Watch it. Write your username in place of `<username>`:

    ```
    qstat -u <username>
    ```

   Expected: a table with one row per job of yours. The column `S` is the state of the job:

   | State | Meaning |
   |---|---|
   | `Q` | Queued: waiting for resources |
   | `R` | Running |
   | `E` | Exiting: it has finished and PBS is cleaning up |

   When the job is finished it disappears from the table. A `Q` for a long time is normal.

7. When the job has finished, look at the folder:

    ```
    ls
    ```

   Expected: besides `job_cpu.pbs` and `POSCAR`, an output file with a name of the form
   `<name>.o<jobid>`, where `<name>` is the job name you chose in step 4. PBS creates this file when the job ends. It holds everything the job
   printed. Read it:

    ```
    cat <name>.o<jobid>
    ```

   Expected: lines of `mlip` output. The run shows `Attaching mace calculator (device=cpu)...` near the start and
   `✅ Optimization complete. Output files:` near the end, followed by one line for six of the files it wrote, each with its full path. In the code of `mliprun`
   these six files are `opt.traj`, `opt.log`, `opt_convergence.csv`, `opt_final.vasp`, `CONTCAR` and `opt_params.txt`, and they are written
   in the folder of the structure, which here is `first_job`. The run also writes `mliprun_run.json`, the run record of module 07, which the list leaves out.
   The line `Optimization complete` appears whether or not the optimization converged. A run that did not converge within the 300
   steps prints, after the file list, a warning that starts with `Warning: Optimization did not converge`. You can also read the result in the file
   `opt_params.txt`, on the line that starts with `Converged:`:

    ```
    grep Converged opt_params.txt
    ```

   Expected: `Converged:         True` or `Converged:         False`.

8. To cancel a job that is queued or running, use its job ID (the number part is enough):

    ```
    qdel <jobid>
    ```

   Check with `qstat -u <username>` that it is gone, or that its state moves to `E`.

## 8. A GPU job

`job_gpu.pbs` is the same as `job_cpu.pbs` except for the job name (`onboarding_gpu`) and two lines that matter:

- the resource request is `select=1:ngpus=1:ncpus=16:mem=64gb`: one GPU, with 16 CPU cores and 64 GB of memory;
- the command ends with `--device cuda` instead of `--device cpu`.

Run it the way section 7 describes: copy `job_gpu.pbs` to a run folder, edit the three
lines of step 4 there (`#PBS -N` the job name, `#PBS -P` the charging code, `MLIP=` the venv path),
`qsub job_gpu.pbs`, and read the output file. From the group's
experience, the queue `normal` sends a request that contains `ngpus` to the GPU queue, so
the queue line does not change. Confirm on first login.

Whether a free account includes GPU hours is not known: confirm whether your allocation includes
GPU hours before you submit a GPU job. A GPU job uses up your free allocation as any other job does (confirm how GPU jobs are charged).

To check that PyTorch sees the GPU, ask for an interactive job with a GPU, load the Python
module and activate the venv, and run `mlip doctor`:

```
qsub -I -P PROJECT_CODE -l select=1:ngpus=1:ncpus=16:mem=64gb -l walltime=00:30:00 -q normal
module load <python module>
source ~/scratch/venv/mlip-mace/bin/activate
mlip doctor
```

Expected: the `CUDA` line says `available (1 device(s))`. If it says `not available`, the
CUDA build of `torch` does not match the GPU node (or the job did not get a GPU); tell your
supervisor. Type `exit` to end the interactive job. Nothing else needs undoing: the venv was
active only inside this job.

When a GPU is worth it, and when not:

Both bullets are the group's rule of thumb, not measured for this module.

- **Worth it, as a rule of thumb:** molecular dynamics (module 10) with many steps, and calculations on large cells.
- **Not worth it, as a rule of thumb:** a small relaxation. The one number available is from module 10: its main run of 400 MD steps on a 45-atom structure took 43.7 to 48.5 s on a laptop CPU. A run that already takes about a minute has little time left to save, and the wait in the GPU queue can be longer than the run itself. A GPU job may also cost more of your free allocation than a CPU job; this was not measured here, so ask your supervisor.

## 9. Move files

**Always make the target folder first.** `rsync` does not create missing parent folders on the remote
side, and it stops with an error that mentions `mkdir` and `No such file or directory`.

`rsync` copies a folder and sends only what changed. **On your laptop** (macOS and Linux), to send a run folder
to ASPIRE2A:

```
ssh <username>@aspire2a.nscc.sg "mkdir -p ~/scratch/onboarding/my_run"
rsync -avz --update my_run/ <username>@aspire2a.nscc.sg:~/scratch/onboarding/my_run/
```

and to bring the results back:

```
rsync -avz --update --exclude '*.traj' <username>@aspire2a.nscc.sg:~/scratch/onboarding/my_run/ my_run/
```

- `-a` keeps the folder structure, `-v` prints each file, `-z` compresses during the transfer.
- `--update` skips a file when the copy at the destination is newer. It also means that a file you edited is skipped if the other side holds a newer one; read the list of files `rsync` prints.
- The trailing `/` on both paths matters: it means "the contents of this folder". Without it, `rsync` makes one more folder level.
- `--exclude '*.traj'` leaves the trajectory files at home. A trajectory such as `md.traj` of module 10 can be large; do not copy it routinely. Copy it only when you need to look at it, and name it.
- The `rsync` that comes with macOS is an old version. It does not know the `--info=` options, and using one prints the whole usage text instead of a clear error. Use `--progress` for progress information, or nothing.
- On Windows, PowerShell does not include `rsync`. Use `scp -r` for a folder, or run the commands above inside WSL (the Linux layer of Windows), if your supervisor has set it up. `scp -r` copies everything, so name the folder you need.

For one file, `scp` is simpler. **On your laptop**:

```
scp <username>@aspire2a.nscc.sg:~/scratch/onboarding/first_job/CONTCAR .
```

The final `.` means "into the folder where I am now". This works the same in PowerShell, macOS Terminal and Linux.

## 10. Before any project job

The job scripts of this module are for learning. Before you submit a job for a research project:

- **The charging code (canon K3).** Every job is charged to an account. For you it is the code that belongs to your free account (section 2); confirm it with your supervisor before the first job, and check it before every submission. CPU hours are counted against the free allocation, so a mistake, such as a wrong request or a job left running, costs your own hours. Do not guess a code or borrow one from another member of the group. Write the code in the `#PBS -P` line; in this module the placeholder `PROJECT_CODE` stands there.
- **The provenance ledger (canon K2).** Every calculation that does not go through the group's managed database is recorded in a ledger: a list of what was run, with which settings. Your supervisor will show you the ledger and how to add a run. Do not skip this step because the job succeeded.
- **The settings are decisions, not defaults.** `mlip optimize run` has built-in values: `--fmax 0.05` and `--max-steps 200`, and its `--mlip` and `--device` options default to `auto`, which means the tool chooses. The `mlip md run` and `mlip neb` commands also have defaults. The tool runs silently with them when you leave an option out; it does not ask. Your job script must therefore carry the project's values for the model, the head, `fmax`, and the MD and NEB settings, as your supervisor records them. If a value for your project is not recorded, ask before you submit.

## 11. When something goes wrong

Start with the output file `<name>.o<jobid>` (section 7) and with `myquota`. Then use this table.

| What you see | Cause | Fix |
|---|---|---|
| A job ends at once, and `qstat` no longer shows it | The script failed at its first command | Read the output file `<name>.o<jobid>`; its last lines name the problem |
| `qsub` refuses the job with a message about the project or the account | The charging code is wrong, missing, or still `PROJECT_CODE` | Use the code of your free account (section 2) and confirm it with your supervisor; edit the `-P` line. The exact words of the message are not recorded here |
| `Disk quota exceeded` | Your home folder is full, usually with caches or large files that went there by mistake | Run `myquota`. Move caches and large files to scratch (`~/scratch`). Section 6 shows how the script redirects them. Never delete files you do not recognise |
| `rsync` fails with `unexpected end of file`, and `ssh` still works | From the group's experience, the usual cause is a full home folder | Run `myquota` before you suspect the network; free space in home; repeat |
| `rsync` stops with a message that mentions `mkdir` and `No such file or directory` | The target folder does not exist on the remote side | Make it first with `ssh <username>@aspire2a.nscc.sg "mkdir -p <folder>"`, then repeat |
| `rsync` on macOS prints a long usage text | An option such as `--info=progress2` is not known to the old `rsync` of macOS | Use `--progress` or no progress option |
| The output file says `.../mlip-mace/bin/mlip: No such file or directory` (or `mlip: command not found` in an interactive session) | The venv path in the job script is wrong, or section 6 did not finish | Check with `ls ~/scratch/venv/mlip-mace/bin/mlip`; correct the `MLIP=` line of the script, or run the setup script again on the login node |
| The output file ends with a message about a missing shared library or a Python library | The job does not know the Python module that the venv was built with | In the job script, remove the `#` before `module load <python module>` and write the module name from section 6 |
| `bad interpreter`, or `$'\r': command not found`, when you run a `.pbs` or `.sh` file | The file can have Windows line endings. A checkout of this repository gets Linux line endings (one line-feed character, `\n`, at the end of each line), but a copy made another way may not. `bash file.sh` prints `$'\r': command not found`; `qsub` may reject a `#PBS` value that ends in a carriage return (the `\r` character) or read it wrongly | On ASPIRE2A, run `sed -i 's/\r$//' <the file>` (section 6 does it for the three files right after copying), then try again |
| A job fails with `PytorchStreamReader failed reading zip archive` or `checkpoint file is corrupted` | The weights download stopped early and left an incomplete file; the download line of the setup script does not check for this | On the login node, delete the file in `~/scratch/.cache/mace/` whose name starts with `20231203mace128L1`, then run the download line again: `python -c "from mace.calculators.foundations_models import download_mace_mp_checkpoint; print(download_mace_mp_checkpoint('medium')); print('OK')"` with the venv active (`source ~/scratch/venv/mlip-mace/bin/activate`) and `export XDG_CACHE_HOME=$HOME/scratch/.cache` set |
| `module: command not found` | The terminal session has not set up the module command | Log out and log in again. If it persists, tell your supervisor |
| `ssh` hangs, then says `Connection timed out` | The host name is wrong, or you are outside the network that can reach ASPIRE2A (section 2, item 7) | Check the welcome email for the host; ask your supervisor about the network or VPN |
| The setup script stops at once with `STOP: no internet connection from the login node`, or fails later with a connection error in `pip install`, `git clone` or the model step | The login node cannot reach the internet, or a proxy or rule blocks that address (confirm with NSCC) | Tell your supervisor, who knows where downloads are allowed |
| The setup script stops with `STOP: run this script on the login node, not inside a job` | You started it inside an interactive job. Compute nodes most likely have no internet (the group's understanding; confirm on first login) | Type `exit` to leave the job, then run the script on the login node |
| A job fails with a connection error or a download message | The job tried to download something, for example the weights of a model that is not yet in your cache | Download it first on the login node (section 6), then submit the job again |
| An email, or a message at login, says your account is blocked | A heavy command ran on the login node (section 5) | Do not try to log in again repeatedly. Tell your supervisor, who contacts NSCC |
| The job stays in `Q` for hours | PBS has no free resources that fit your request | Normal at busy times. A smaller request and a shorter walltime start earlier. Ask your supervisor before you change a project job |
