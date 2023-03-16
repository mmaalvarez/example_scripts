#!/bin/bash
#SLURM --mem=7G

conda activate bowtie2


# The reference genome stored locally
REF=hg19_chrom.fa

# Build the bowtie2 index for the reference genome
bowtie2-build $REF $REF

# Build IGV index for the reference genome
samtools faidx $REF


### output: *.bt2 (bowtie2) and .fai (IGV index) 7 files are for using them to align fastq files to (in this case) hg19 and create bam files; if chipseq, bams will be used to compare signal vs. input's signal, as in /g/strcombio/fsupek_cancer3/malvarez/chromatin_info/DNA_repair__protein_binding/DNA_repair/MMR/MSH6_SETD2_H3K36me3_guominli/1_alignment/bin/align.sh
