import ntpath
import os
import pandas as pd, seaborn as sns
import scipy.spatial as sp, scipy.cluster.hierarchy as hc
import matplotlib.pyplot as plt


class ClustermapVisualizer(object):
    def __init__(self, distance_dataframe, linkage_method, distance_dataframe_aux=None,
                 linkage_method_aux=None, scaling=None):
        self._linkage_method = linkage_method
        self._distance_dataframe = distance_dataframe
        self._distance_dataframe_aux = distance_dataframe_aux
        self._linkage_method_aux = linkage_method_aux
        self._scaling = scaling

    def run(self, title=None, filename=None):
        df = self._distance_dataframe
        squareform = sp.distance.squareform(self._distance_dataframe)
        linkage = hc.linkage(squareform, method=self._linkage_method)
        linkage_aux = linkage
        if self._distance_dataframe_aux is not None:
            squareform_aux = sp.distance.squareform(self._distance_dataframe_aux)
            linkage_aux = hc.linkage(squareform_aux, method=self._linkage_method_aux)
            df = PairwiseDistanceMatrix.combine(self._distance_dataframe, self._distance_dataframe_aux)
        cm = sns.clustermap(df, row_linkage=linkage, col_linkage=linkage_aux)
        custom_title = title
        if custom_title is None:
            if filename is None:
                custom_title = ''
            else:
                custom_title = self._path_leaf(filename)
        self._format_plot(cm, custom_title)
        self._scale(cm.fig)
        self._possibly_save_plot(cm, filename)

    def _format_plot(self, cm, title):
        cm.fig.suptitle(title)
        plt.setp(cm.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        plt.setp(cm.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)

    def _possibly_save_plot(self, cm, filename):
        if filename is not None:
            fig = cm.fig
            fig.savefig(filename)

    def _scale(self, fig):
        if self._scaling is not None:
            scalting_alt = 1 - self._scaling
            fig.subplots_adjust(left=self._scaling, bottom=self._scaling, right=scalting_alt, top=scalting_alt)

    def _path_leaf(self, path):
        head, tail = ntpath.split(path)
        out = tail or ntpath.basename(head)
        filename, file_extension = os.path.splitext(out)
        return filename
