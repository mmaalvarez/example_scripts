#!/usr/bin/env nextflow


// this runs in parallel for each fastq file

fastq_files = Channel.from(params.fastq_files.tokenize(','))

process align_fastqs_into_bams {

    publishDir "$PWD/bam_output/", mode: 'move'

    time = { params.time.hour }
    memory = { (params.memory + 5*(task.attempt-1)).GB }

    input:
    val fastq_file from fastq_files
    path fastq_path from params.fastq_path
    val ref_genome from params.ref_genome

    output:
    file '*.bam*'

    """
    #!/usr/bin/env bash

    conda activate bowtie2

    # Run the bowtie2 aligner. Creates a SAM file, piped into sorted BAM format
    bowtie2 -x ${ref_genome} -U ${fastq_path}/${fastq_file}_pass.fastq.gz | samtools sort -o ${fastq_file}.bam -
    
    # Index the BAM file
    samtools index ${fastq_file}.bam
    """
}
