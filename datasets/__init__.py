import os
from enum import Enum

import pandas as pd

from data_model.dataset import Table

TT_CATEGORIES = {'ALL': ([], []),
                 'CTRL_WIKI': (['WIKI'], ['NOISE2']),
                 'CTRL_DBP': (['CTRL', 'DBP'], ['NOISE2']),
                 'CTRL_NOISE2': (['CTRL', 'NOISE2'], []),
                 'TOUGH_T2D': (['T2D'], ['NOISE2']),
                 'TOUGH_HOMO': (['HOMO'], ['SORTED', 'NOISE2']),
                 'TOUGH_MISC': (['MISC'], ['NOISE2']),
                 'TOUGH_MISSP': (['MISSP'], ['NOISE1', 'NOISE2']),
                 'TOUGH_SORTED': (['SORTED'], ['NOISE2']),
                 'TOUGH_NOISE1': (['NOISE1'], []),
                 'TOUGH_NOISE2': (['TOUGH', 'NOISE2'], [])
                 }


# class GTEnum(Enum):
#     """
#     Enumerate the datasets available in the benchmark
#     """
#     ST19_Round_1 = 'Round1'
#     ST19_Round_2 = 'Round2'
#     ST19_Round_3 = 'Round3'
#     ST19_Round_4 = 'Round4'
#     TT = '2T'
#
#     def get_df(self):
#         """
#         Load the dataset in a Pandas dataframe
#         :return: a dataframe
#         """
#         return pd.read_csv(os.path.join(os.path.dirname(__file__), self.value),
#                            dtype={'table': str, 'col_id': int, 'row_id': int, 'label': str,
#                                   'context': str, 'entities': str},
#                            keep_default_na=False)
#
#     def get_table_categories(self):
#         """
#         Return the set of relevant categories for a specific dataset.
#         For each category, a pair of keywords (to_include, to_exclude) is provided to
#         filter the rows relevant to the category.
#         :return: a dictionary Dict(category, Tuple(to_include, to_exclude))
#         """
#         if self == self.CEA_TT:
#             return TT_CATEGORIES
#         return {'ALL': ([], [])}
#
#     @classmethod
#     def get_test_gt(cls, size, from_gt=None, random=False):
#         """
#         Helper method to generate a test dataset on-the-fly.
#         :param size: dimension of the test dataset to create
#         :param from_gt: dataset to sample rows from
#         :param random: True if the rows should be sampled randomly; otherwise, the top ``size`` rows are returned.
#         :return: a Pandas dataframe
#         """
#         if from_gt is None:
#             from_gt = cls.CEA_Round1
#         if random:
#             df = from_gt.get_df().sample(size).reset_index()
#         else:
#             df = from_gt.get_df()[:size]
#         tmp = Enum('GTTestEnum', {'%s_TEST_%drows' % (from_gt.name, size): df})  # create a temp enum (name: df)
#         setattr(tmp, 'get_df', lambda x: x.value)  # add the get_df function, that returns the df
#         setattr(tmp, 'get_table_categories', lambda x: {'ALL': ([], [])})
#         return list(tmp)[0]
#
#     @classmethod
#     def get_test_tt_by_type(cls, type_, size=0):
#         """
#         Helper method to generate a test dataset on-the-fly, from the 2T ground truth.
#         :param type_: optionally filter entries by type (e.g., dbo:Person).
#         :param size: dimension of the test dataset to create
#         :return: a Pandas dataframe
#         """
#         df = cls.CEA_TT.get_df()
#         df2 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'CTA_TT.csv'))
#         df2 = df2[df2['type'] == type_]
#         df = df.merge(df2, on=['table', 'col_id'], how='inner').drop(columns=['type'])
#         if size > 0:
#             df = df.sample(size).reset_index()
#
#         tmp = Enum('GTTestEnum', {'CEA_TT_%s' % type_[type_.rindex("/") + 1:]: df})
#         setattr(tmp, 'get_df', lambda x: x.value)
#         setattr(tmp, 'get_table_categories', lambda x: TT_CATEGORIES)
#         return list(tmp)[0]


class DatasetEnum(Enum):
    """
    Enumerate the datasets available in the benchmark
    """
    ST19_Round1 = 'Round1'
    ST19_Round2 = 'Round2'
    ST19_Round3 = 'Round3'
    ST19_Round4 = 'Round4'
    TT = '2T'
    T2D = 'T2D'

    def _target_path(self, task):
        return f"{os.path.dirname(__file__)}/{self.value}/targets/{task}_{self.value}_Targets.csv"

    def _gt_path(self, task):
        return f"{os.path.dirname(__file__)}/{self.value}/gt/{task}_{self.value}_gt.csv"

    def _table_path(self, tab_id):
        return f"{os.path.dirname(__file__)}/{self.value}/tables/{tab_id}.csv"

    # def get_target_cells(self):
    #     if not os.path.exists(self._target_path('CEA')):
    #         return {}
    #
    #     target = pd.read_csv(self._target_path('CEA'),
    #                          names=['tab_id', 'col_id', 'row_id'],
    #                          dtype={'tab_id': str, 'col_id': int, 'row_id': int})
    #     return {k: [Cell(*pair) for pair in zip(v['row_id'], v['col_id'])] for k, v in target.groupby('tab_id')}
    #
    # def get_target_columns(self):
    #     if not os.path.exists(self._target_path('CTA')):
    #         return {}
    #
    #     target = pd.read_csv(self._target_path('CTA'),
    #                          names=['tab_id', 'col_id'],
    #                          dtype={'tab_id': str, 'col_id': int})
    #     return {k: [Column(col_id) for col_id in v['col_id']] for k, v in target.groupby('tab_id')}
    #
    # def get_target_column_relations(self):
    #     if not os.path.exists(self._target_path('CPA')):
    #         return {}
    #
    #     target = pd.read_csv(self._target_path('CPA'),
    #                          names=['tab_id', 'source_id', 'target_id'],
    #                          dtype={'tab_id': str, 'source_id': int, 'target_id': int})
    #     return {k: [ColumnRelation(*pair) for pair in zip(v['source_id'], v['target_id'])]
    #             for k, v in target.groupby('tab_id')}

    # def get_tables(self):
    #     with os.scandir(f"{os.path.dirname(__file__)}/{self.value}/tables") as it:
    #         for entry in it:
    #             if entry.name.endswith(".csv"):
    #                 yield Table(os.path.splitext(entry.name)[0], self.value, entry.path)

    def get_tables(self):
        cea = pd.read_csv(self._gt_path('CEA'),
                          names=['tab_id', 'col_id', 'row_id', 'entities'],
                          dtype={'tab_id': str, 'col_id': int, 'row_id': int, 'entities': str})
        cea['entities'] = cea['entities'].apply(str.split)
        cta_groups = None
        if os.path.exists(self._gt_path('CTA')):
            cta = pd.read_csv(self._gt_path('CTA'),
                              names=['tab_id', 'col_id', 'types'],
                              dtype={'tab_id': str, 'col_id': int, 'types': str})
            cta['types'] = cta['types'].apply(str.split)
            cta_groups = cta.groupby('tab_id')
        cpa_groups = None
        if os.path.exists(self._gt_path('CPA')):
            cpa = pd.read_csv(f"{os.path.dirname(__file__)}/{self.value}/gt/CPA_{self.value}_gt.csv",
                              names=['tab_id', 'source_id', 'target_id', 'properties'],
                              dtype={'tab_id': str, 'source_id': int, 'target_id': int, 'properties': str})
            cpa['properties'] = cpa['properties'].apply(str.split)
            cpa_groups = cpa.groupby('tab_id')

        cea_groups = cea.groupby('tab_id')
        for tab_id, cea_group in cea_groups:
            table = Table(tab_id, self.value, self._table_path(tab_id))
            table.set_gt_cell_annotations(zip(cea_group['row_id'], cea_group['col_id'], cea_group['entities']))
            if cta_groups and tab_id in cta_groups.groups:
                cta_group = cta_groups.get_group(tab_id)
                table.set_gt_column_annotations(zip(cta_group['col_id'], cta_group['types']))
            if cpa_groups and tab_id in cpa_groups.groups:
                cpa_group = cpa_groups.get_group(tab_id)
                table.set_gt_property_annotations(zip(cpa_group['source_id'],
                                                      cpa_group['target_id'],
                                                      cpa_group['properties']))

            yield table

    # def get_df(self):
    #     """
    #     Load the dataset in a Pandas dataframe
    #     :return: a dataframe
    #     """
    #     return pd.read_csv(os.path.join(os.path.dirname(__file__), self.value),
    #                        dtype={'table': str, 'col_id': int, 'row_id': int, 'label': str,
    #                               'context': str, 'entities': str},
    #                        keep_default_na=False)

    def get_table_categories(self):
        """
        Return the set of relevant categories for a specific dataset.
        For each category, a pair of keywords (to_include, to_exclude) is provided to
        filter the rows relevant to the category.
        :return: a dictionary Dict(category, Tuple(to_include, to_exclude))
        """
        if self == self.TT:
            return TT_CATEGORIES
        return {'ALL': ([], [])}

    # @classmethod
    # def get_test_dataset(cls, size, from_gt=None, rand=False):
    #     """
    #     Helper method to generate a test dataset on-the-fly.
    #     :param size: dimension of the test dataset to create
    #     :param from_gt: dataset to sample rows from
    #     :param rand: True if the rows should be sampled randomly; otherwise, the top ``size`` rows are returned.
    #     :return: a Pandas dataframe
    #     """
    #     if from_gt is None:
    #         from_gt = cls.ST19_Round1
    #     targets = from_gt.get_targets()
    #     gt = from_gt.get_gt_tables()
    #     table_ids = list(targets)
    #     if rand:
    #         random.shuffle(table_ids)
    #     cells = []
    #     for tab_id in table_ids:
    #         cells.append(table_ids[tab_id])
    #     while len(cells) < size:
    #         df = from_gt.get_df().sample(size).reset_index()
    #     else:
    #         df = from_gt.get_df()[:size]
    #     tmp = Enum('GTTestEnum', {'%s_TEST_%drows' % (from_gt.name, size): df})  # create a temp enum (name: df)
    #     setattr(tmp, 'get_df', lambda x: x.value)  # add the get_df function, that returns the df
    #     setattr(tmp, 'get_table_categories', lambda x: {'ALL': ([], [])})
    #     return list(tmp)[0]
    #
    # @classmethod
    # def get_test_tt_by_type(cls, type_, size=0):
    #     """
    #     Helper method to generate a test dataset on-the-fly, from the 2T ground truth.
    #     :param type_: optionally filter entries by type (e.g., dbo:Person).
    #     :param size: dimension of the test dataset to create
    #     :return: a Pandas dataframe
    #     """
    #     df = cls.CEA_TT.get_df()
    #     df2 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'CTA_TT.csv'))
    #     df2 = df2[df2['type'] == type_]
    #     df = df.merge(df2, on=['table', 'col_id'], how='inner').drop(columns=['type'])
    #     if size > 0:
    #         df = df.sample(size).reset_index()
    #
    #     tmp = Enum('GTTestEnum', {'CEA_TT_%s' % type_[type_.rindex("/") + 1:]: df})
    #     setattr(tmp, 'get_df', lambda x: x.value)
    #     setattr(tmp, 'get_table_categories', lambda x: TT_CATEGORIES)
    #     return list(tmp)[0]