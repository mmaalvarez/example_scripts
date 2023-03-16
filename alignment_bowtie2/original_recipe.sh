#!/bin/bash

conda activate bowtie2


## from bioinformatics.recipes/recipe/view/recipe-bowtie/#code

# Stop on errors.
set -uex

# Reference genome accession number (this example is Ebola virus)
ACC=AF086833

# The SRR number for the input sequencing data (in this example, fasta file)
SRR=SRR1972739

# How many reads to unpack
N=10000

# The reference genome stored locally.
REF=refs/$ACC.fa

# The directory that store the reference.
mkdir -p refs

# Get the reference genome in FASTA format.
efetch -db nuccore -format fasta -id $ACC > $REF

# Build the bowtie2 index for the reference genome.
bowtie2-build $REF $REF  1>> log.txt 2>> log.txt

# Build IGV index for the reference genome.
samtools faidx $REF

# Obtain the FASTQ sequences for the SRR number.
fastq-dump -X $N --split-files $SRR  >> log.txt

# The name for the read pairs (only if paired end)
R1=${SRR}_1.fastq
R2=${SRR}_2.fastq

## Run the bowtie2 aligner. Creates a SAM file
# if paired-end data
bowtie2 -x $REF -1 $R1 -2 $R2 -S $SRA.sam
# if non-paired end (-U)
bowtie2 -x $REF -U ${SRR}.fastq.gz -S $SRA.sam

# Convert the SAM file to sorted BAM format
cat $SRR.sam | samtools sort > $SRR.bam

# Index the BAM file.
samtools index $SRR.bam

#Generate an alignment report.
samtools flagstat $SRR.bam > alignment-report.txt
