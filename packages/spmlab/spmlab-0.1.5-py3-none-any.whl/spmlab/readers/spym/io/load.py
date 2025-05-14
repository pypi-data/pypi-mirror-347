import os
from . import rhksm4

def load(filename, scaling=True):
    ''' Import data from common SPM file formats.

    Currently supported file formats are:
        * NeXus (.nx, .nxs). Package nxarray is needed.
        * RHK (.sm4).
        * Omicron Scala (.par).

    Args:
        filename: path to the SPM file.
        scaling: if True convert data to physical units (default), if False keep raw data.

    Returns:
        xarray Dataset with data and metadata.

    '''
    if filename.endswith(".sm4") or filename.endswith(".SM4"):
        try:
            ds = rhksm4.to_dataset(filename, scaling=scaling)
        except:
            print("Error: the file does not appear to be valid.")
            return None

    for dr in ds:
        ds[dr].attrs["filename"] = os.path.basename(filename)

    return ds
