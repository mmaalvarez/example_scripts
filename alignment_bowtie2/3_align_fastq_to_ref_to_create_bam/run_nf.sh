#!/bin/bash

#export TOWER_ACCESS_TOKEN="eyJ0aWQiOiA0ODk1fS4yNDdkNzEyYmY5NGUxMmFlOTQ1OGYwYWJlYmI2MjY0YmU2Y2E4Yzdl"

# define where the ref genome files for bowtie2 are placed (it looks for $BOWTIE2_INDEXES)
export BOWTIE2_INDEXES=/g/strcombio/fsupek_cancer3/malvarez/hg_fasta/hg19/bowtie2/

mkdir -p log/

nextflow -log $PWD/log/nextflow.log run pipe.nf --ref_genome hg19_chrom.fa \
												--fastq_files SRR13314138,SRR13314132,SRR13314133,SRR13314134,SRR13314135 \
												--fastq_path $PWD/../2_download_SRA_fastq/fastq_SRA/fastq/ \
												--time 4 \
												--memory 8 \
												-resume #-with-tower \
# SRR13314138	input
# SRR13314132	MSH6-0mM
# SRR13314133	MSH6-1mM
# SRR13314134	SETD2-0mM
# SRR13314135	SETD2-1mM
