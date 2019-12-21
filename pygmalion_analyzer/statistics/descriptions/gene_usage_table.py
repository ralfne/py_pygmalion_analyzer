from bayesian_network_utilities.api.bayesian_network_wrapper import BayesianNetworkWrapper, ProbabilityType
from pygmalion.donors.iterator import GenModelWrapperIterator, DonorIterator
import immune_receptor_utils.gene as ir_gene
import immune_receptor_utils.genes as ir_genes
from pygmalion.genmodel.nicknames import Nicknames
import pandas as pd
import numpy as np


class MarginalGeneUsageTable(object):
    def __init__(self, donors_list, genes=None, filtering_chain=None):
        self._donors_list = donors_list
        self._genes = genes
        self._filtering_chain = filtering_chain

    def run(self):
        self._prepare_genes()
        itr = DonorIterator(self._donors_list)
        data = []
        donors = []
        for donor in itr:
            donors.append(donor.get_name())
            gu = self._get_gene_usage_for_donor(donor)
            data.append(gu)
        gene_names = self._get_genenames_as_list(self._genes)
        out = pd.DataFrame(data=data, index=donors, columns=gene_names)
        out = out.transpose()
        out = self._add_stat_functions(out)
        return out

    def _add_stat_functions(self, df):
        df['mean'] = df.mean(numeric_only=True, axis=1)
        df['max'] = df.max(numeric_only=True, axis=1)
        df['min'] = df.min(numeric_only=True, axis=1)
        df['std.dev.'] = df.std(numeric_only=True, axis=1, ddof=0)
        return df

    def _get_genenames_as_list(self, genes):
        out = []
        for g in genes:
            out.append(str(g))
        return out

    def _get_gene_usage_for_donor(self, donor):
        out = []
        for gene in self._genes:
            p = self._get_probability_for_gene(donor, gene)
            out.append(p)
        return out

    def _get_probability_for_gene(self, donor, gene):
        out = self._get_probability_for_gene_and_nickname(donor, gene, str(Nicknames.v_choice.value))
        if out is None:
            out = self._get_probability_for_gene_and_nickname(donor, gene, str(Nicknames.j_choice.value))
        if out is None:
            out = self._get_probability_for_gene_and_nickname(donor, gene, str(Nicknames.d_gene.value))
        return out

    def _get_probability_for_gene_and_nickname(self, donor, gene, nickname):
        itr_gmw = GenModelWrapperIterator(donor)
        for gmw in itr_gmw:
            statename = gmw.get_eventname_for_nickname(nickname)
            if statename is not None:
                network_wrapper = gmw.get_bayesian_network_wrapper()
                probabilities = network_wrapper.get_probabilities(statename, ProbabilityType.Marginal)
                gene_id = str(gene)
                if not nickname in gene_id:
                    gene_id = nickname + ':' + gene_id
                if probabilities.index.contains(gene_id):
                    out = probabilities.loc[gene_id]
                    return out
        return None

    def _prepare_genes(self):
        if self._genes is None:
            self._genes = self._get_all_genes()
        elif not isinstance(self._genes, ir_genes.GenePossibilities):
            self._genes = self._convert_to_gene_possibilities(self._genes)

    def _convert_to_gene_possibilities(self, items):
        out = ir_genes.GenePossibilities()
        for item in items:
            gene = ir_gene.Gene(str(item), assume_01_allele=False)
            out.add_gene(gene)
        return out

    def _get_all_genes(self):
        gene_possibilities = ir_genes.GenePossibilities()
        self._filtering_genes = self._add_filtering_genes(str(Nicknames.v_choice.value), gene_possibilities)
        self._filtering_genes = self._add_filtering_genes(str(Nicknames.j_choice.value), gene_possibilities)
        self._filtering_genes = self._add_filtering_genes(str(Nicknames.d_gene.value), gene_possibilities)
        return gene_possibilities

    def _add_filtering_genes(self, nickname, gene_possibilities):
        itr = DonorIterator(self._donors_list)
        for donor in itr:
            itr_gmw = GenModelWrapperIterator(donor, self._filtering_chain)
            for gmw in itr_gmw:
                statename = gmw.get_eventname_for_nickname(nickname)
                if statename is not None:
                    network_wrapper = gmw.get_bayesian_network_wrapper()
                    probabilities = network_wrapper.get_probabilities(statename, ProbabilityType.Marginal)
                    for key, row in probabilities.iteritems():
                        gene = ir_gene.Gene(key, assume_01_allele=False)
                        gene_possibilities.add_gene(gene, also_check_allele=True)
            # One donor contains all genes we need
            break



