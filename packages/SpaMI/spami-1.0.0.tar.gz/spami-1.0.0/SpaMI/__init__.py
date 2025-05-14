from .main import train
from .model import SpaMI
from .preprocess import preprocess_rna, preprocess_rna_h5, preprocess_atac, preprocess_atac_h5, preprocess_adt, preprocess_adt_h5
from .utils import leiden_cluster

__version__ = "1.0.0"