from pygmalion_analyzer.clustering.clustermap_feature_visualizer import ClustermapFeatureVisualizer
import seaborn as sns


class ClustermapDistanceVisualizer(ClustermapFeatureVisualizer):
    def __init__(self,  distance_dataframe, linkage_method='average', scaling=None):
        super(ClustermapDistanceVisualizer, self).__init__(distance_dataframe, None, linkage_method, scaling)

    def _run_clustermap(self, df, row_linkage):
        cm = sns.clustermap(self._distance_dataframe, row_linkage=row_linkage)
        return cm
