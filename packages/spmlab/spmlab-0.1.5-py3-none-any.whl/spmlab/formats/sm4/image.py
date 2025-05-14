## Typing
from enum import Enum
from warnings import warn

## External packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import gridspec
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from xarray import DataArray, Dataset
from pathlib import Path


class TopoDirection(Enum):
    Forward, Backward = range(2)


class TopoData:
    """
    """
    def __init__(self, src: str, ds: DataArray):
        self.path = Path(src)
        self.name = self.path.stem
        self.ds = ds
        self.data = ds.data

    def plot(self,
             fig=None,
             align=True, 
             plane=True, 
             fix_zero=True, 
             show_axis=False,
             show_title=False,
             show_scalebar=True,
             scalebar_height=None,
             figsize=(8,8), 
             cmap=plt.cm.afmhot):
        """
        """
        img = self.ds

        if align:
            img.spym.align()
        if plane:
            img.spym.plane()
        if fix_zero:
            img.spym.fixzero()
        
        if fig is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            n = len(fig.axes)
            gs = gridspec.GridSpec(1, n+1)
            # Reposition existing subplots
            for i, ax in enumerate(fig.axes):
                ax.set_position(gs[i].get_position(fig))
                ax.set_subplotspec(gs[i])

            # Add new subplot
            ax = fig.add_subplot(gs[n])

        if not show_axis:
            ax.axis('off')
        else:
            ax.set_xlabel("[nm]")
            ax.set_ylabel("[nm]")

        size = round(img.RHK_Xsize * abs(img.RHK_Xscale) * 1e9, 3)
        if scalebar_height is None:
            scalebar_height = 0.01 * size
        fontprops = fm.FontProperties(size=14)
        scalebar = AnchoredSizeBar(ax.transData,
                                   size/5, f'{size/5} nm', 'lower left',
                                   pad=0.25,
                                   color='white',
                                   frameon=False,
                                   size_vertical = scalebar_height,
                                   offset=1,
                                   fontproperties=fontprops)

        ax.imshow(img.data, extent=[0, size, 0, size], cmap=cmap)
        
        if show_scalebar:
            ax.add_artist(scalebar)

        if show_title:
            ax.set_title('topo data: ' + self.name)

        fig.tight_layout()
        return (fig, ax)


    def get_min(self) -> float:
        """
        """
        return np.min(self._topo.data)


    def get_max(self) -> float:
        """
        """
        return np.max(self._topo.data)


class ImageData:
    """
        ImageData is a container for the forward and backward topography data coming from src.
        Technically an AbstractSM4Data subclass, but doesn't implement the abstract methods
        and instead holds two references to other AbstractSM4Data subclasses (TopoData)
    """
    def __init__(self, src: str, ds: Dataset):
        self.path = Path(src)
        self.name = self.path.stem
        self.forward = TopoData(src, ds.Topography_Forward)
        self.backward = TopoData(src, ds.Topography_Backward)

    def plot(self):
        raise Exception(("\nCannot call plot() on ImageData object.\n" 
                         "Please call plot() on the forward or backward attributes:\n"
                         "---------------------------------------------------------\n"
                         "from spmlab.formats import sm4\n" 
                         "topo = sm4.read(\"path/to/topo/data.sm4\")\n"
                         "topo.forward.plot()\n"))