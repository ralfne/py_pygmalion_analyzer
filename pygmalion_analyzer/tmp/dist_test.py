from Logger import StdOutLogger
from bayesian_network_utilities.api.bayesian_network_wrapper import ProbabilityType
from pygmalion.donors.iterator import GenModelWrapperIterator
from pygmalion.genmodel.nicknames import Nicknames
from pygmalion.persistence.default_persistence_handler import DefaultPersistenceHandler
from scipy.spatial import distance
import immune_receptor_utils.enums as ir
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial.distance import squareform
import immune_receptor_utils.enums as ir

from pygmalion_analyzer.clustering.clustermap_distance_visualizer import ClustermapDistanceVisualizer
from pygmalion_analyzer.clustering.marginals_feature_matrix import MarginalsFeatureMatrix
from pygmalion_analyzer.clustering.clustermap_feature_visualizer import ClustermapFeatureVisualizer
from pygmalion_analyzer.distances.calculators import SpatialCDistCalculator, JensenShannonCalculator, \
    EuclideanDistanceCalculator
import seaborn as sns
import scipy.spatial as sp, scipy.cluster.hierarchy as hc

fn = 'C:/CiR/pTCR/IGOR_models/Unproductive_models/models_imgt_ref_dir_sep2019/HC'
donors_hc = DefaultPersistenceHandler.instantiate(fn, StdOutLogger(verbose=True))
itr = GenModelWrapperIterator(donors_hc,filtering_chain=ir.Chain.TRB)
for gmw in itr:
    gmw.merge_alleles()

features = MarginalsFeatureMatrix(items=donors_hc, nicknames=[str(Nicknames.v_choice.value)], chain=ir.Chain.TRB)

calc = SpatialCDistCalculator('minkowski', p=2)
#calc = JensenShannonCalculator()
#calc = EuclideanDistanceCalculator()
dist_df = calc.run(features.df)
viz = ClustermapFeatureVisualizer(dist_df, features.df, linkage_method='average', scaling=None)
#viz = ClustermapPairwiseVisualizer(dist_df, linkage_method='average', scaling=None)
viz.run('title', None)

plt.show()

exit(0)


d_1363 = donors_hc.get_donor('1363_')
d_1365 = donors_hc.get_donor('1365_')
d_1450 = donors_hc.get_donor('1450_')

d_1363_bnw = d_1363.get_genmodel_wrapper(ir.Chain.TRA).get_bayesian_network_wrapper()
d_1365_bnw = d_1365.get_genmodel_wrapper(ir.Chain.TRA).get_bayesian_network_wrapper()
d_1450_bnw = d_1450.get_genmodel_wrapper(ir.Chain.TRA).get_bayesian_network_wrapper()
key = d_1363.get_genmodel_wrapper(ir.Chain.TRA).get_eventname_for_nickname(str(Nicknames.v_choice.value))
u = d_1363_bnw.get_probabilities(statename=key, probability_type=ProbabilityType.Marginal)
v = d_1365_bnw.get_probabilities(statename=key, probability_type=ProbabilityType.Marginal)
w = d_1450_bnw.get_probabilities(statename=key, probability_type=ProbabilityType.Marginal)
#u = [1,4,6]
#v = [6,7,8]
x = pd.concat([u,v, w], axis=1)
x=x.transpose()
out = distance.pdist(X=x, metric='minkowski', p=2)
print out
out = squareform(out)

#
# df (rows = donors/gmws, columns=gene usage etc):
#     bayesian_network_wrapper.get_probabilities(statename=None, probability_type=ProbabilityType.Marginal)
#
#
# scipy.spatial.distance:
# two array-like as input()
#
#
#
# from scipy.spatial.distance import pdist
# pdist(df.loc[['1363_', '1365_']])
# array([342.3024978])
#
#
# from scipy.spatial.distance import squareform
#
# squareform(pdist(df.loc[['1363_', '1365_', '1450_']]))
# array([[  0.        , 342.3024978 , 317.98584874],
#        [342.3024978 ,   0.        , 144.82403116],
#        [317.98584874, 144.82403116,   0.        ]])
#
#
# pd.DataFrame(
#     squareform(pdist(summary.loc[['Germany', 'Italy', 'France']])),
#     columns = ['Germany', 'Italy', 'France'],
#     index = ['Germany', 'Italy', 'France']
# )
# 	Germany	Italy	France
# Germany	0.000000	342.302498	317.985849
# Italy	342.302498	0.000000	144.824031
# France	317.985849	144.824031	0.000000
#
#
# pairwise = pd.DataFrame(
#     squareform(pdist(summary)),
#     columns = summary.index,
#     index = summary.index
# )
#
# pairwise
#
#
# Country	Afghanistan	Algeria	Argentina	...	Yugoslavia	Zambia	Zimbabwe
# Country
# Afghanistan	0.000000	8.774964	96.643675	...	171.947666	1.732051	17.492856
# Algeria	8.774964	0.000000	95.199790	...	171.688672	7.348469	19.519221