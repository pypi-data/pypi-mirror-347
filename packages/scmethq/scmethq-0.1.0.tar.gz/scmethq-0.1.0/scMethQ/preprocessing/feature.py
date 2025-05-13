import numpy as np
from ..io import *


def sliding_windows(window_size, ref=None,step_size=None, chrom_file=None):
    """

    :param window_size:
    :param step_size:
    :param ref:
        A Genome object, providing gene annotation and chromosome sizes. ref should be one of `hg38,hg19,mm10,mm9,GRCh37,GRCh38,GRCm39`
        `genome` has lower priority than `gff_file` and `chrom_size`.
    :param chrom_file:
        File name of the gene annotation file in BED or GFF or GTF format.
        This is required if `ref` is not set.
        Setting `chrom_file` will override the annotations from the `genome` parameter.
    :param chrom_size:
        A dictionary containing chromosome sizes, for example,
        `{"chr1": 2393, "chr2": 2344, ...}`.
        This is required if `genome` is not set.
        Setting `chrom_size` will override the chrom_size from the `genome` parameter.
    :return:
    """
    chrom_size_dict = {}
    
    if step_size is None:
        step_size = window_size
    if chrom_file is None:
        if ref is not None:
            chrom_size_dict = ref.chrom_sizes
    else:
        chrom_size_dict = load_chrom_size_file(chrom_file)  # user defined reference, especially for other species
    features_dict = {}
    for chrom, chrom_length in chrom_size_dict.items():
        bin_start = np.array(list(range(1, chrom_length, step_size)))
        bin_end = bin_start + window_size - 1
        bin_end[np.where(bin_end > chrom_length)] = chrom_length
        chrom_ranges = [(start, end) for start, end in zip(bin_start, bin_end)]
        features_dict[chrom]= chrom_ranges  
    return features_dict

def load_features(feature_file,format=None):
    #TO DO: load features from gtf file or gff file
    features_dict = {}
    if format==None:
        input_file_format = feature_file[-3:]
    if input_file_format=="bed":
        features_dict = read_annotation_bed(feature_file)
    # elif input_file_format=='gtf':
    #     features_dict = load_features_gtf(feature_file,feature_type="gene")
    # elif input_file_format=='gff':
    #     features_dict = load_features_gff(feature_file,feature_type="gene")
    # elif input_file_format=='csv':
    #     features_dict = load_features_csv(feature_file)
    else:
        raise ValueError("Unsupported file format")
    return features_dict    
