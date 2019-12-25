from pygmalion_analyzer.clustering.clustermap_feature_visualizer import ClustermapFeatureVisualizer
import seaborn as sns

from pygmalion_analyzer.figures.figure_parameters import ClusteringFigureParameters


class ClustermapDistanceVisualizer(ClustermapFeatureVisualizer):
    def __init__(self,  distance_dataframe, linkage_method='average', clustering_figure_parameters=ClusteringFigureParameters()):
        super(ClustermapDistanceVisualizer, self).__init__(distance_dataframe, None, linkage_method, clustering_figure_parameters)

    def _run_clustermap(self, df, row_linkage):
        cm = sns.clustermap(self._distance_dataframe, row_linkage=row_linkage, col_cluster=False)
        return cm
