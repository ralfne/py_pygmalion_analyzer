import ntpath
import os
import scipy as sp
import scipy.spatial as sp, scipy.cluster.hierarchy as hc
import seaborn as sns
import matplotlib.pyplot as plt


class ClustermapFeatureVisualizer(object):
    def __init__(self,  distance_dataframe, features_dataframe, linkage_method='average', scaling=None):
        self._linkage_method = linkage_method
        self._distance_dataframe = distance_dataframe
        self._features_dataframe = features_dataframe
        self._scaling = scaling

    def run(self, title=None, filename=None):
        squareform = sp.distance.squareform(self._distance_dataframe)
        linkage = hc.linkage(squareform, method=self._linkage_method)
        cm = self._run_clustermap(self._features_dataframe, linkage)
        custom_title = title
        if custom_title is None:
            if filename is None:
                custom_title = ''
            else:
                custom_title = self._path_leaf(filename)
        self._format_plot(cm, custom_title)
        self._scale(cm.fig)
        self._possibly_save_plot(cm, filename)

    def _run_clustermap(self, df, row_linkage):
        cm = sns.clustermap(df, row_linkage=row_linkage)
        return cm

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
