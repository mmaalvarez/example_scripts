mkdir sra fastq

for SRA in SRR13314138 SRR13314132 SRR13314133 SRR13314134 SRR13314135
do
	sbatch sratoolkit_download_fastq_from_SRA.sh $SRA
done
