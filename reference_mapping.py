################################################################
# Script para mapeo de referencia de los reads generados con ONT#
################################################################

import os


def referencemapping(reference, reads):
    os.system(f"minimap2 -a -x map-ont {reference}.fasta {reads}*.fastq > output.sam")


def fixmate():
    os.system("samtools fixmate -O bam,level=1 output.sam fixmate.bam")


def dupmark():
    os.system("samtools fixmate -O bam,level=1 -m output.sam fixmate.bam")


def posorder():
    os.system("samtools sort -l 1 -@8 -o pos.srt.bam -T /tmp/temp fixmate.bam")


def dupmark2():
    os.system("samtools markdup -O bam,level=1 pos.srt.bam markdup.bam")


def bamformat(archivobam):
    os.system(f"samtools view -@8 markdup.bam -o {archivobam}.bam")


def igvvis(archivobam):
    os.system(f"samtools index {archivobam}.bam  {archivobam}.bam.bai")


def consensus(archivobam):
    os.system(
        f"samtools consensus -f fasta {archivobam}.bam -o {archivobam}_consensus.fasta"
    )


def main():
    reference = input(
        "Ingrese el nombre del archivo fasta de referencia (Sin extensión): "
    )
    reads = input("Ingrese reads (Nombre consenso, sin extensión): ")
    archivobam = input("Ingrese el nombre del archivo de salida (Sin extensión): ")
    referencemapping(reference, reads)
    fixmate()
    dupmark()
    posorder()
    dupmark2()
    bamformat(archivobam)
    igvvis(archivobam)
    consensus(archivobam)


main()

os.remove("fixmate.bam")
os.remove("markdup.bam")


"""Cómo archivos de salida tengo que tener:
1. Archivo.bam
2. Archivo.bam.bai
3. Secuencia_consenso.fasta
"""
