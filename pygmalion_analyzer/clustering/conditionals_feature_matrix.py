from bayesian_network_utilities.api.bayesian_network_wrapper import ProbabilityType
import pandas as pd
from pygmalion_analyzer.clustering.marginals_feature_matrix import MarginalsFeatureMatrix


class ConditionalsFeatureMatrix(MarginalsFeatureMatrix):
    def __init__(self, items, nicknames, chain=None):
        super(ConditionalsFeatureMatrix, self).__init__(items=items, nicknames=nicknames,chain=chain)

    def _get_series_for_nicknames(self, genmodel_wrapper, bn_wrapper):
        series = []
        for nickname in self._nicknames:
            event_name = genmodel_wrapper.get_eventname_for_nickname(nickname)
            df = bn_wrapper.get_probabilities(statename=event_name, probability_type=ProbabilityType.Conditional)
            s = self._transform_conditional_df_to_series(df.copy())
            s = s.sort_index()
            series.append(s)
        out = pd.concat(series, axis=0)
        return out

    def _transform_conditional_df_to_series(self, df):
        df['name'] = df['outcome'] + '; ' + df['conditions']
        df.drop('conditions', axis='columns', inplace=True)
        df.drop('outcome', axis='columns', inplace=True)
        df.set_index('name', inplace=True)
        return df['p']