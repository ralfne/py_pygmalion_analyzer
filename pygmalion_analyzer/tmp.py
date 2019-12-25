from Logger import StdOutLogger
from pygmalion.donors.donors import Donors
from pygmalion.donors.iterator import GenModelWrapperIterator
from pygmalion.persistence.default_persistence_handler import DefaultPersistenceHandler

from pygmalion_analyzer.statistics.descriptions.gene_usage_table import MarginalGeneUsageTable
import pandas as pd

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
fn = 'C:/CiR/pTCR/IGOR_models/Unproductive_models/models_imgt_ref_dir_sep2019/HC'
donors_hc = DefaultPersistenceHandler.instantiate(fn, logger)
d_1363 = donors_hc.get_donor('1363_')
d_1365 = donors_hc.get_donor('1365_')
itr = GenModelWrapperIterator([d_1363, d_1365])

# for gmw in itr:
#     gmw.merge_alleles(events=None, prefixes=None, assert_merge_definitions=False)
genes = ['TRBV11-3*01','TRBV5-1*01', 'TRBV6-8*01', 'TRBV9*01']
tbl = MarginalGeneUsageTable([[d_1363, d_1365]], None)
tbl.run()

print 34
