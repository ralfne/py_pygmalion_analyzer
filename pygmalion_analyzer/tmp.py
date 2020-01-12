from Logger import StdOutLogger
from pygmalion.donors.donors import Donors
from pygmalion.donors.iterator import GenModelWrapperIterator
from pygmalion.genmodel.nicknames import Nicknames
from pygmalion.persistence.default_persistence_handler import DefaultPersistenceHandler
from pygmalion_analyzer.distances.calculators import JensenShannonCalculator

from pygmalion_analyzer.clustering.marginals_feature_matrix import MarginalsFeatureMatrix

from pygmalion_analyzer.statistics.descriptions.gene_usage_table import MarginalGeneUsageTable
import pandas as pd
import immune_receptor_utils.enums as ir

s = pd.Series(data=[1,2,3,4], index=['a','c','b','x'])
s = s.sort_index()

logger = StdOutLogger(verbose=False)

# fn = 'C:/CiR/pTCR/IGOR_models/Unproductive_models/models_imgt_ref_dir_sep2019/CeD/1424_TRB'
# donors1 = DefaultPersistenceHandler.instantiate(fn, logger)
# fn = 'C:/CiR/pTCR/IGOR_models/Unproductive_models/models_imgt_ref_dir_sep2019/CeD/1416_TRB'
# donors2 = DefaultPersistenceHandler.instantiate(fn, logger)
# donors = Donors(logger)
# donors.add_donor(donors1.get_donor_from_index(0))
# donors.add_donor(donors2.get_donor_from_index(0))
#
# tbl = MarginalGeneUsageTable([donors])
# tbl.run()

# fn = 'C:/CiR/pTCR/IGOR_models/Unproductive_models/models_imgt_ref_dir_sep2019/CeD'
# donors_ced = DefaultPersistenceHandler.instantiate(fn, logger)

def create_v_del_features():
    d = {'del1': [0.8, 0.1, 0.7], 'del2': [0.2, 0.9, 0.3]}
    out = pd.DataFrame(data=d, index=['d1', 'd2', 'd3'])
    return out

def create_v_gene_features():
    d = {'v1': [0.4, 0.6, 0.1], 'v2': [0.1, 0.3, 0.6], 'v3': [0.5, 0.1, 0.3]}
    out = pd.DataFrame(data=d, index=['d1', 'd2', 'd3'])
    return out

def create_combined(dfs, weights):
    for df, weight in zip(dfs, weights):
        for col in df.columns:
            #c = c * weight
            df[col] = df[col] * weight
    out = pd.concat(dfs, axis=1)
    return out

def calc_separate(calculator, dfs, weights):
    out = 0.0
    for df, weight in zip(dfs, weights):
        x = calculator.run(df)
        x = x * weight
        out += x
    return out


def calc_combined(calculator, df):
    out = calculator.run(df)
    return out


def transform_into_distribution(dfs):
    out = []
    for df in dfs:
        series = []
        df['factor'] = 1/df.sum(axis=1)
        cols=[]
        for n,c in df.iteritems():
            cols.append(n)
            c = c * df['factor']
            series.append(c)
        newdf = pd.concat(series, axis=1)
        newdf.columns = cols
        newdf.drop('factor', axis=1, inplace=True)
        out.append(newdf)
        print 6
    return out


def print_results(df1, df2):
    index = list(df1.index.values)
    for i in range(0,len(index)-1):
        for j in range(i+1,len(index)):
            c=index[i]
            r=index[j]
            v1 = df1.loc[c, r]
            v2 = df2.loc[c, r]
            print str(v1) + ' - ' + str(v2)


weights = [0.5 ,0.5]
df_v_gene = create_v_gene_features()
df_v_del = create_v_del_features()
df_comb = create_combined([df_v_gene, df_v_del], weights)
calc = JensenShannonCalculator(base=2)

df_comb = transform_into_distribution([df_comb])

x_comb = calc_combined(calc, df_comb[0])
x_sep = calc_separate(calc, [df_v_gene, df_v_del], weights)

print_results(x_sep, x_comb)

exit(-1)

fn = 'C:/CiR/pTCR/IGOR_models/Unproductive_models/models_imgt_ref_dir_sep2019/HC'
donors_hc = DefaultPersistenceHandler.instantiate(fn, logger)
f = MarginalsFeatureMatrix(donors_hc,nicknames=[Nicknames.vj_dinucl.value,
                                                Nicknames.vj_ins.value,
                                                Nicknames.v_choice.value],
                                                chain=ir.Chain.TRA)
f = MarginalsFeatureMatrix(donors_hc,nicknames=[Nicknames.vd_dinucl.value,
                                                Nicknames.dj_dinucl.value,
                                                Nicknames.vd_ins.value,
                                                Nicknames.dj_ins.value,
                                                Nicknames.v_choice.value],
                                                chain=ir.Chain.TRB)
print f


d_1363 = donors_hc.get_donor('1363_')
d_1365 = donors_hc.get_donor('1365_')
itr = GenModelWrapperIterator([d_1363, d_1365])

# for gmw in itr:
#     gmw.merge_alleles(events=None, prefixes=None, assert_merge_definitions=False)
genes = ['TRBV11-3*01','TRBV5-1*01', 'TRBV6-8*01', 'TRBV9*01']
tbl = MarginalGeneUsageTable([[d_1363, d_1365]], None)
tbl.run()

print 34
