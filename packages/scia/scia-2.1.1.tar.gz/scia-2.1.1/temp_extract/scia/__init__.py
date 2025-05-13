# Dynamically retrieve version from setuptools-scm
try:
    from ._version import __version__
except ModuleNotFoundError:
    # If running from source, use setuptools-scm
    try:
        from setuptools_scm import get_version
        __version__ = get_version(root='..', relative_to=__file__)
    except:
        __version__ = "dev"  # Fallback for development mode

# Print a message when the package is imported
print(f"📖 scia {__version__} - For Documentation, visit: https://ahsankhodami.github.io/scia/intro.html")

from .data import create_scd
from .fill_missing import fill_missing
from .filter import subset_scd
from .io import read_scd, write_scd
from .ird import ird
from .pand import pand
from .pem import pem
from .pet import pet
from .plm import plm
from .pnd import pnd
from .preprocess import prepare_scd
from .recombine import recombine_phases
from .select import select_cases
from .smd import smd
from .summary import summary
from .tau_u import tau_u
from .utils import revise_names
from .autocorr import autocorr
from .corrected_tau import corrected_tau
from .nap import nap
from .overlap import overlap
# from .select import select_cases  # Remove duplicate import
from .as_data_frame import as_data_frame
from .describe import describe
from .prepare_scdf import prepare_scdf
from .check_scdf import check_scdf
from .hplm import hplm
from .check_args import *
from .print_hplm import print_hplm
from .rci import rci
from .std_lm import std_lm
from .mplm import mplm
from .plot import plot