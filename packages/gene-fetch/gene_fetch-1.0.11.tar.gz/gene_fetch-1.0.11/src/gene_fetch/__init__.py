"""
Gene Fetch - NCBI Sequence Retrieval Tool

This package fetches sequence data from NCBI databases
using sample taxonomic information.
"""

__version__ = "1.0.7"

from .core import Config
from .entrez_handler import EntrezHandler
from .sequence_processor import SequenceProcessor
from .output_manager import OutputManager, save_genbank_file

# Expose main entry point for usage
from .main import main