from abc import ABCMeta, abstractmethod
from scipy.spatial import distance
import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform
from scipy.stats import entropy


class DistanceCalculator(object):
    __metaclass__ = ABCMeta

    def __init__(self):pass

    @abstractmethod
    def run(self, data):pass


class SpatialCDistCalculator(DistanceCalculator):
    def __init__(self, metric, **kwargs):
        super(SpatialCDistCalculator, self).__init__()
        self._metric = metric
        self._kwargs = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                self._kwargs[key] = value

    def run(self, data):
        out = distance.pdist(data, self._metric,  **self._kwargs)
        pairwise = pd.DataFrame(squareform(out), columns=data.index, index=data.index)
        return pairwise


class JensenShannonCalculator(DistanceCalculator):
    def __init__(self):
        super(JensenShannonCalculator, self).__init__()

    def run(self, data):
        out = NotImplementedError
        if isinstance(data, pd.DataFrame):
            out = self._get_pairs(data)
        else:
            raise NotImplementedError()
        return out

    def _get_pairs(self, data):
        index = data.index
        l_index = len(index)
        out = np.zeros((l_index, l_index))
        for i in range(l_index - 1):
            for j in range(i+1, l_index):
                s0 = data.loc[index[i]]
                s1 = data.loc[index[j]]
                y = self._run_for_series(s0, s1)
                out[i,j] = y
        i_lower = np.tril_indices(l_index, -1)
        out[i_lower] = out.T[i_lower]
        out = pd.DataFrame(out, index = index, columns=index)
        return out


    def _run_for_series(self, series1, series2):
        out = JensenShannonCalculator.calculate_jensen_shannon(series1, series2, 2)
        return out

    @staticmethod
    def calculate_jensen_shannon(p, q, base):
        # could not install scipy version 1.5 which contains the jensen-shannon func;
        # using solution from https://gist.github.com/zhiyzuo/f80e2b1cfb493a5711330d271a228a3d
        p = np.asarray(p)
        q = np.asarray(q)
        # normalize
        p /= p.sum()
        q /= q.sum()
        m = (p + q) / 2
        return (entropy(p, m, base=base) + entropy(q, m, base)) / 2



class EuclideanDistanceCalculator(DistanceCalculator):
    def __init__(self):
        super(EuclideanDistanceCalculator, self).__init__()

    def run(self, data):
        out = NotImplementedError
        if isinstance(data, pd.DataFrame):
            out = self._get_pairs(data)
        else:
            raise NotImplementedError()
        return out

    def _get_pairs(self, data):
        index = data.index
        l_index = len(index)
        out = np.zeros((l_index, l_index))
        for i in range(l_index - 1):
            for j in range(i+1, l_index):
                s0 = data.loc[index[i]]
                s1 = data.loc[index[j]]
                y = self._run_for_series(s0, s1)
                out[i,j] = y
        i_lower = np.tril_indices(l_index, -1)
        out[i_lower] = out.T[i_lower]
        out = pd.DataFrame(out, index = index, columns=index)
        return out


    def _run_for_series(self, series1, series2):
        out = distance.euclidean(series1, series2)
        return out

