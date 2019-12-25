from bayesian_network_utilities.api.bayesian_network_wrapper import ProbabilityType
from pygmalion.donors.iterator import GenModelWrapperIterator
import pandas as pd


class MarginalsFeatureMatrix(object):
    def __init__(self, items, nicknames, chain=None):
        self._items = items
        self._chain = chain
        self._nicknames = nicknames
        self.df = self._create_df()

    def _create_df(self):
        series = []
        itr = GenModelWrapperIterator(self._items, filtering_chain=self._chain)
        names = []
        for gmw in itr:
            bn_wrapper = gmw.get_bayesian_network_wrapper()
            events_serie = self._get_series_for_nicknames(gmw, bn_wrapper)
            series.append(events_serie)
            names.append(gmw.get_name())
        df = pd.concat(series, axis=1)
        df = df.transpose()
        df.index = names
        return df

    def _get_series_for_nicknames(self, genmodel_wrapper, bn_wrapper):
        series = []
        for nickname in self._nicknames:
            event_name = genmodel_wrapper.get_eventname_for_nickname(nickname)
            s = bn_wrapper.get_probabilities(statename=event_name, probability_type=ProbabilityType.Marginal)
            s = s.sort_index()
            series.append(s)
        out = pd.concat(series, axis=0)
        return out
