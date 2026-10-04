.. _before-begin:

***************
Before we begin
***************


BASH
####

Before you start with the tutorial, you will find here the Bash Shell commands that you will need to manage directories and files, inspect sequence data, and **run the same analysis on several genomes** without typing each command by hand.

.. note::
   Shell is an interface that accepts commands and delivers them to the operating system to perform.
   UNIX-based operating systems (Linux, macOS, and others) can have different Shell types (e.g., Bash, zsh).

This intro focuses on the Bash Shell. However, since macOS Catalina (10.15) the default shell of macOS is **zsh**. Everything shown in this tutorial works the same way in both shells.

.. note::
   Lines starting with ``$`` show the **prompt**; you must not type the ``$`` itself. Everything after a hash ``#`` is a comment and is ignored by the shell.


Exploring the Terminal
**********************

First, you need to look for your Terminal, the program that allows you to interact with the Shell.

Open the Terminal as explained below:

* If you're on a Mac, you'll find the Terminal under Applications -> Utilities. The easiest way is to press 'command + space' which will bring up Spotlight, and then you can write Terminal.
* If you're on a Linux then you will probably find it in Applications -> System or Applications -> Utilities.

.. attention::
   Yet, if you have a Windows-based system, you will need to install a Shell and a Terminal.
   First, be sure that you have all the Windows 10 (version 2004 or higher) or Windows 11 upgrades performed.
   Second, open ``PowerShell`` as administrator and run ``wsl --install``, as explained in the `Windows Subsystem for Linux (WSL) <https://learn.microsoft.com/en-us/windows/wsl/install>`_ official page.
   Finally, reboot your computer and your new Terminal will appear as ``Ubuntu``.

   If you are working with the WSL, remember that if you want to access the ``Documents`` folder of Windows you should write on the command line ``/mnt/c/Users/XXX/Documents`` instead of ``\Users\XXX\Documents``. However, for better performance, keep your tutorial files inside the Linux home directory (``~``).

   Additionally, if you want to open locally the current folder just write on the command line ``explorer.exe .``

Whenever you open a Terminal, you will see your last login credentials and a Shell prompt.
The appearance might vary a little, but usually, you will see the username@machinename followed by a ``$`` (bash) or ``%`` (zsh) sign.

.. figure:: ./images/Terminal.png
	 :figclass: align-left

*Figure 2. This is an example of a macOS Terminal.*


Basic Bash Commands
*******************

Try to run in the Terminal some of the basic Bash commands and look at the output. Below you can see handy comments for users that were added after the hash ``#`` mark and are ignored by Bash.

.. note::
   In most of these examples, you shouldn't forget to write in the command line what is the file or directory that you want to move, remove, create, or copy.

.. hint::
   Press the **Tab** key to auto-complete file and directory names, and the **up/down arrows** to browse the commands that you have already used. Press **Ctrl + C** to stop a running command.


**A. Change Directory (cd) commands**

.. code-block:: bash

   # Navigate between directories on your computer
   # In this case, it will go to Documents directory
   $ cd Documents/

   # Display the current directory (print working directory)
   $ pwd

   # Stay in the current directory ("." means "here")
   $ cd .

   # Go back to the directory above
   $ cd ..

   # Go back to the previous directory where you were
   $ cd -

   # Go back to the home directory
   $ cd ~

   # Go to the root of the file system
   $ cd /


**B. List (ls) commands**

.. code-block:: bash

  # Print a list of files and subdirectories within directories
  $ ls

  # Print the contents of a specific directory
  # In this case, it prints the Desktop content
  $ ls Desktop/

  # List all the files, including the hidden ones (starting with a dot)
  $ ls -a

  # Print a more detailed list of files
  $ ls -l

  # Print a detailed list with human-readable file sizes (e.g., 5.4M) sorted by size
  $ ls -lhS

  # Regardless of what directory you are into it will always list your home directory
  $ ls ~

  # List only the files with a specific extension (* is a wildcard)
  $ ls *.fasta


**C. Organizing files and directories**

.. code-block:: bash

    # Create a new directory (mkdir)
    $ mkdir <folder_name1>

    # Create a directory and all the missing parent directories (mkdir -p)
    $ mkdir -p tutorial/raw_data

    # Create several directories at once using brace expansion
    $ mkdir -p tutorial/{raw_data,qc_visualisation,assembly,annotation}

    # Used to create empty new files (touch)
    $ touch <filename1> <filename2>

    # Moves one or more files from one directory to another (mv)
    # You need to specify the <source_file> and the <destination> directory
    $ mv <source_file> <destination>

    # Rename a file (mv)
    $ mv <old_name> <new_name>

    # Delete a file (rm)
    # Be careful: there is no recycle bin in the shell, deleted files cannot be recovered!
    $ rm <filename1>

    # Ask for confirmation before deleting (rm -i)
    $ rm -i <filename1>

    # Delete directories and every file inside it (rm -r)
    $ rm -r <folder_name1>

    # Remove empty directories (rmdir)
    $ rmdir <folder_name1>

    # Copy files to another directory (cp)
    # You need to specify the <source_file> to be copied and the <destination> directory
    $ cp <source_file> <destination>

    # Copy a directory and its contents to another directory (cp -r)
    $ cp -r <folder_name1> <folder_name2>

    # Create a shortcut (symbolic link) to a file without duplicating it (ln -s)
    # Useful to avoid copying large files, such as fastq files
    $ ln -s ~/tutorial/raw_data/strainA_R1.fastq.gz strainA_R1.fastq.gz

    # Find files by name inside a directory and its subdirectories (find)
    $ find ~/tutorial -name "*.fasta"


**D. Viewing and exploring file content**

.. code-block:: bash

   # Display the first 10 lines of a created file (head)
   $ head -n 10 <filename1>

   # Display the last 10 lines of a created file (tail)
   $ tail -n 10 <filename1>

   # Concatenate or join two or more files into a single one (cat)
   $ cat <filename1>.txt <filename2>.txt > <filename3_join>.txt

   # Count the number of lines, words and characters of a file (wc)
   $ wc <filename1>
   $ wc -l <filename1>

   # Search for patterns in a file (grep)
   # Extract the lines that match the '>' symbol, in this case the headers
   $ grep '>' NC_002695.2.fasta

   # Count how many sequences a multi-fasta file has
   $ grep -c '>' <filename1>.fasta

   # Search for a nucleotide sequence and print 1 line before and after any match
   $ grep -B 1 -A 1 'GAGGTTGTTGAAATCGA' NC_002695.2.fasta

   # View content of a created file (less)
   # Press the space bar to scroll down, / to search, and q to exit less
   $ less <filename1>

   # View the content of a compressed file without uncompressing it (gunzip -c)
   # (zcat also works on Linux, but on macOS you need to use gunzip -c)
   $ gunzip -c <filename1>.fastq.gz | head -n 8

   # Edit content of a created file (nano)
   # Press Ctrl + O to save and Ctrl + X to exit nano
   $ nano <filename1>


**E. Other useful commands**

.. code-block:: bash

   # Clear the terminal screen
   $ clear

   # Print the current working directory
   $ pwd

   # Print the processes that are using more of the computer resources (press q to exit)
   $ top

   # Print the number of available CPUs (useful to set the number of threads of a tool)
   $ nproc               # Linux/WSL
   $ sysctl -n hw.ncpu   # macOS

   # Print the free disk space and the size of a directory
   $ df -h
   $ du -sh ~/tutorial

   # Download files from the internet using a link (wget)
   # You need to specify the <link_source> to the file
   $ wget <link_source>

   # Alternatively, you can use curl (installed by default on macOS)
   $ curl -L -O <link_source>

   # Display the manual of a command (press q to exit)
   $ man ls

   # Show where a program is installed
   $ which python

   # Show the history of the commands that you have already used
   $ history

.. seealso::
   You can also use a semicolon ``;`` character to write two commands on the same line, or ``&&`` to run the second command only if the first one finishes successfully.

   If you have a very long command you can run separate code chunks onto separate lines by using the ``\`` character (with nothing after it) to make it more readable.


**F. Redirection and pipes**

Most bash commands print the results on the screen (the **standard output**). You can save these results in a file or send them directly to another command.

.. code-block:: bash

   # Save the output of a command in a new file (>)
   # Warning: if the file already exists it will be overwritten
   $ grep '>' NC_002695.2.fasta > headers.txt

   # Add the output to the end of an existing file (>>)
   $ echo "strainA" >> samples.txt
   $ echo "strainB" >> samples.txt

   # Use the output of one command as the input of the next one (|), called a pipe
   # This counts the number of reads of a compressed fastq file (4 lines per read)
   $ gunzip -c strainA_R1.fastq.gz | wc -l | awk '{print $1/4}'

   # Save the error messages (standard error) in a separate log file (2>)
   $ fastqc strainA_R1.fastq.gz 2> fastqc.log

   # Save both the output and the error messages in the same file (&>)
   $ fastqc strainA_R1.fastq.gz &> fastqc.log


**G. Working with tables and text**

Many bioinformatics tools produce **tab-separated** (``.tsv``, ``.tab``, ``.txt``) tables. The following commands will help you to explore them quickly.

.. code-block:: bash

   # Print only some columns of a tab-separated table (cut)
   # In this case, the 1st, 6th, and 10th columns
   $ cut -f 1,6,10 results.tsv

   # Sort a file alphabetically (sort) or numerically (sort -n), and in reverse order (-r)
   $ sort results.tsv
   $ sort -k2,2nr results.tsv     # sort by the 2nd column, numerically and in reverse order

   # Remove duplicated lines (uniq only works on sorted files)
   $ cut -f 1 results.tsv | sort | uniq

   # Count how many times each different value appears
   $ cut -f 6 results.tsv | sort | uniq -c | sort -nr

   # Print the lines of a table in which a column fulfils a condition (awk)
   # In this case, the lines where the 10th column is higher than 90
   $ awk -F '\t' '$10 > 90' results.tsv

   # Print the header (first line) and skip it in the following commands (tail -n +2)
   $ head -n 1 results.tsv
   $ tail -n +2 results.tsv | wc -l

   # Replace a text in each line of a file (sed)
   $ sed 's/NC_002695.2/Sakai/g' NC_002695.2.fasta > Sakai.fasta

   # Translate characters (tr), in this case the complement of each nucleotide
   $ echo "ATGC" | tr 'ACGT' 'TGCA'

   # Print a table with aligned columns on the screen (column)
   $ column -t -s $'\t' results.tsv | less -S


**H. Variables and loops: running a command in several genomes**

When you have several samples, you do not need to retype the same command for each one. You can use **variables** and **loops** to repeat it.

.. code-block:: bash

   # Create a variable (no spaces around the = sign) and print its content ($)
   $ sample=strainA
   $ echo $sample
   $ echo "Analysing ${sample}_R1.fastq.gz"

   # Save the output of a command in a variable ($(...))
   $ today=$(date +%Y-%m-%d)
   $ echo $today

   # Run the same command in a list of samples (for loop)
   $ for sample in strainA strainB; do echo "Analysing $sample"; done

   # Run a command in all the files with a given extension
   $ for file in ~/tutorial/genomes/*.fasta; do echo $file; done

   # Remove the directory and the extension of a file name
   # basename removes the directory, and the second argument removes the extension
   $ file=~/tutorial/genomes/strainA.fasta
   $ basename $file .fasta       # strainA

   # Read the sample names from a text file, one per line (while loop)
   $ while read -r sample; do echo "Analysing $sample"; done < samples.txt

   # Use an if statement to skip a sample if the output already exists
   $ for sample in strainA strainB; do
   >    if [ -s results/${sample}.tsv ]; then echo "$sample already done"; continue; fi
   >    echo "Running $sample"
   > done

.. note::
   When a command is typed in several lines (as in the ``if`` example), the shell shows the ``>`` symbol at the beginning of each continuation line. You do not need to type it.

.. hint::
   Always **quote** your variables (e.g., ``"$sample"``) when they can contain spaces. Before running a long loop, put ``echo`` in front of the command (e.g., ``echo fastqc $file``) to see what would be executed (a **dry run**).

A variable defined in the shell is only available in that terminal window. Use ``export`` to make it available to the programs that you run, and add it to the file ``~/.bashrc`` (Linux/WSL) or ``~/.zshrc`` (macOS) if you want to keep it permanently.

.. code-block:: bash

   # Create an environment variable
   $ export TUTORIAL=~/tutorial
   $ ls $TUTORIAL

   # See the directories where the shell looks for programs
   $ echo $PATH


**I. Shell scripts**

If you want to keep and reuse a set of commands, write them in a text file, called a **script**, instead of typing them in the terminal.

.. code-block:: bash

   # Create a script with nano
   $ nano count_reads.sh

   # Content of the script count_reads.sh
   #!/usr/bin/env bash
   # Usage: bash count_reads.sh sample1_R1.fastq.gz sample2_R1.fastq.gz ...
   set -euo pipefail          # stop the script if a command fails

   for file in "$@"; do       # "$@" are all the arguments given to the script
       lines=$(gunzip -c "$file" | wc -l)
       echo -e "${file}\t$((lines / 4))"
   done

   # Run the script
   $ bash count_reads.sh ~/tutorial/raw_data/*_R1.fastq.gz

   # Make the script executable and run it directly
   $ chmod +x count_reads.sh
   $ ./count_reads.sh ~/tutorial/raw_data/*_R1.fastq.gz


**J. Running long jobs, permissions and compression**

.. code-block:: bash

   # Run a long command in the background and keep it running after you close the terminal (nohup)
   # The output is saved in nohup.log; the final & sends the command to the background
   $ nohup bash my_pipeline.sh > nohup.log 2>&1 &

   # See the jobs running in the background and your running processes
   $ jobs
   $ ps aux | grep unicycler

   # Stop a process using its ID (PID)
   $ kill <PID>

   # See the file permissions (r = read, w = write, x = execute)
   $ ls -l

   # Give execution permission to a file
   $ chmod +x <filename1>

   # Compress and uncompress a single file
   $ gzip <filename1>.fastq
   $ gunzip <filename1>.fastq.gz

   # Compress an entire directory into one file, and extract it (tar)
   $ tar -czvf results.tar.gz results/
   $ tar -xzvf results.tar.gz

   # Compress/uncompress .zip files
   $ zip -r results.zip results/
   $ unzip results.zip

   # Copy files to/from another computer or server (scp, rsync)
   $ scp results.tar.gz user@server:/path/to/destination/
   $ rsync -avh --progress user@server:/path/to/results/ ~/tutorial/results/

   # Compare the integrity of a downloaded file (checksum)
   $ md5sum <filename1>      # Linux/WSL
   $ md5 <filename1>         # macOS


**K. Good practices**

* Do not use **spaces** or special characters (e.g., ``ç``, ``ã``, ``(``) in file and directory names. Use underscores ``_`` or dashes ``-`` instead.
* Never overwrite or edit your **raw data**. Create a copy or work with new output files.
* Use **descriptive and consistent names** for samples (e.g., ``strainA``) and keep one directory per analysis step.
* Always **read the log files and error messages**; most of the problems are due to wrong file paths, missing files, or lack of disk space/memory.
* Keep a record of the **commands, tool versions** and **databases versions** used in your analysis (e.g., using ``history > commands.txt``, ``conda list --export > packages.txt``).


Further Reading
***************

This small tutorial is only a little start to basic Bash commands. However, you will see in the future that they will bring you a lot of advantages and benefits.
If you want to dig a little bit more about specific or advanced Bash commands, I leave here some available online resources and books:

* `UNIX Tutorial for Beginners <http://www.ee.surrey.ac.uk/Teaching/Unix/>`_
* `The Linux Command Line <http://linuxcommand.org/tlcl.php>`_
* `Beginner's Guide to the Bash Terminal <https://www.youtube.com/watch?v=oxuRxtrO2Ag>`_
* `bash Cookbook <https://www.amazon.com/bash-Cookbook-Solutions-Examples-Users/dp/1491975334/>`_
* `Learning the bash Shell <https://www.amazon.com/Learning-bash-Shell-Programming-Nutshell-ebook/dp/B0043GXMSY/>`_
* `The Biostar Handbook: 2nd Edition <https://www.biostarhandbook.com/index.html>`_
