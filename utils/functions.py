import re
import string
from typing import List
from typing import Tuple, Dict, Set

import numpy as np
from dateutil.parser import parse
from scipy.spatial.distance import cosine
from sklearn.preprocessing import MinMaxScaler

from data_model.generator import ScoredCandidate, CandidateEmbeddings


def chunk_list(list_, chunk_size):
    """
    Utility function to split a list into chunks of size chunk_size.
    The last chunk might be smaller than chunk_size.
    :param list_: the list to split
    :param chunk_size: chunk length
    :return: a generator of lists of size chunk_size
    """
    for i in range(0, len(list_), chunk_size):
        yield list_[i:i + chunk_size]


def strings_subsequences(strings: List[str], max_subseq_len) -> Tuple[Dict[str, List[str]], Set[str]]:
    """
    Given a list of strings, this method computes all the subsequences of different lengths, up to ``max_subseq_len``.
    Returns a tuple with a Dict(label: List(subsequences)) to preserve the mapping label-subsequence,
    and the set with all the subsequences.
    :param strings: a list of strings
    :param max_subseq_len: length of the longest subsequence to compute
    :return: a tuple (<subsequences_dict>, <subsequences_set>)
    """
    subsequences = {}
    subsequences_set = set()
    for string in strings:
        tokens = string.split()
        subsequences[string] = [" ".join(tokens[:i + 1])
                                for i in reversed(range(min(max_subseq_len, len(tokens))))]
        subsequences_set.update(subsequences[string])
    return subsequences, subsequences_set


def weighting_by_ranking(candidates: List[CandidateEmbeddings], alpha=0.5, default_score=None) -> List[ScoredCandidate]:
    """
    Rank the candidates accordingly with the cosine distance between their vectors
    and their original ranks. If the default_score is provided, instances with one or more missing embeddings
    are assigned that score; otherwise, these instances are not considered and pushed at the end of the ranked list,
    following the original rank.
    :param candidates: a list of CandidateEmbeddings
    :param alpha: a value in [0.0, 1.0], which represents the weight of the original rank component.
           1 - alpha is the weight of the cosine distance.
    :param default_score: default score >= 0.0 to assign to instances with missing embeddings
    :return: a list of ScoredCandidate ranked by score
    """

    if default_score:
        assert default_score >= 0.0
    assert 0.0 <= alpha <= 1.0

    scored_candidates = []
    non_scored_candidates = []
    for rank, c_emb in enumerate(candidates):
        if c_emb.context_emb is not None and c_emb.abstract_emb is not None:
            scored_candidates.append(ScoredCandidate(c_emb.candidate,
                                                     rank,
                                                     cosine(c_emb.context_emb, c_emb.abstract_emb),
                                                     None))
        elif default_score:
            scored_candidates.append(ScoredCandidate(c_emb.candidate,
                                                     rank,
                                                     default_score,
                                                     None))
        else:
            # keep the original order, but push all of them at the end
            non_scored_candidates.append(ScoredCandidate(c_emb.candidate,
                                                         rank,
                                                         None,
                                                         None))

    if not candidates or not scored_candidates:  # safe guard
        return non_scored_candidates  # empty or all candidates are non-scored candidates

    rank_scaler = MinMaxScaler()
    distance_scaler = MinMaxScaler()
    rank_scaler.fit(np.arange(len(candidates)).reshape(-1, 1))
    distance_scaler.fit(np.array([c.distance for c in scored_candidates]).reshape(-1, 1))

    scored_candidates = map(
        lambda s_cand: ScoredCandidate(s_cand.candidate,
                                       s_cand.original_rank,
                                       s_cand.distance,
                                       alpha * rank_scaler.transform([[s_cand.original_rank]])[0][0]
                                       + (1 - alpha) * distance_scaler.transform([[s_cand.distance]])[0][0]),
        scored_candidates)
    return sorted(scored_candidates, key=lambda s_cand: s_cand.score) + non_scored_candidates


def _remove_dates(input_str):
    """
    Remove dates from a string.
    :param input_str: a string
    :return:
    """
    s = re.sub(r'([a-zA-Z]+)([0-9]+)', r'\1 \2', input_str)  # split tokens like 2011-11-29November -> 2011-11-29 November
    s = re.sub(r'([0-9]+)([a-zA-Z]+)', r'\1 \2 ', s)  # split tokens like November2011 -> November 2011

    tokens = s.split()
    f = []
    for token in tokens:
        try:
            parse(token)
        except:
            try:
                parse(re.sub(f"[{string.punctuation}]", '', token))  # try to remove also symbols (like ?3,600 -> 3600)
            except:
                f.append(token)

    return " ".join(f)


def _remove_single_char(input_str):
    return " ".join(filter(lambda x: len(x) > 1, input_str.split()))


def _remove_numbers(input_str):
    return " ".join(filter(lambda x: not x.isnumeric(), input_str.split()))


def _remove_brackets(input_str):
    """
    Remove brackets content (if it starts in the first 5 tokens).
    E.g.:
    - _remove_brackets("Barack Hussein Obama II (US /bəˈrɑːk huːˈseɪn oʊˈbɑːmə/; born August 4, 1961)")
      > Barack Hussein Obama II
    - _remove_brackets("Del Piero (pronunciation: [del ˈpjɛːro]) Ufficiale OMRI (born 9 November 1974)") ->
      > Del Piero  Ufficiale OMRI (born 9 November 1974)
    - _remove_brackets("Alessandro Del Piero Ufficiale OMRI (born 9 November 1974)")
      > Alessandro Del Piero Ufficiale OMRI (born 9 November 1974)
    :param input_str:
    :return:
    """
    s = input_str
    max_pos = len(" ".join(s.split()[:5]))
    if '(' in s and ')' in s and s.index('(') < max_pos:
        s = s[0:s.index('(')] + s[s.index(')') + 1:]
    return s


def simplify_string(input_str, dates=True, numbers=True, single_char=True, brackets=True):
    s = input_str
    if brackets:
        s = _remove_brackets(s)
    if dates:
        s = _remove_dates(s)
    if numbers:
        s = _remove_numbers(s)
    if single_char:
        s = _remove_single_char(s)
    return s
