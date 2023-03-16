#!/bin/bash
#SBATCH --partition=normal_prio
#SBATCH --mem=4G

SRA=$1

# download the SRA file associated with the specified SRA run ID
prefetch $SRA --output-directory sra

# extract the contents of SRA into a .fastq.gz file
fastq-dump --outdir fastq --gzip --skip-technical --readids --read-filter pass --dumpbase --split-3 --clip sra/"$SRA"/"$SRA".sra

# --gzip: Compress output using gzip. Gzip archived reads can be read directly by bowtie2.
# --skip-technical: Dump only biological reads, skip the technical reads.
# --readids or -I: Append read ID after spot ID as ‘accession.spot.readid’. With this flag, one sequence gets appended the ID .1 and the other .2. Without this option, pair-ended reads will have identical IDs.
# --read-filter pass: Only returns reads that pass filtering (without Ns).
# --dumpbase or -B: Formats sequence using base space (default for other than SOLiD). Included to avoid colourspace (in which pairs of bases are represented by numbers).
# --split-3 separates the reads into left and right ends. If there is a left end without a matching right end, or a right end without a matching left end, they will be put in a single file.
# --clip or -W: Some of the sequences in the SRA contain tags that need to be removed. This will remove those sequences.
# --outdir or -O: (Optional) Output directory, default is current working directory.