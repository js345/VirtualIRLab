"""
Referenced from https://github.com/meta-toolkit/metapy-demos
"""

import time
import metapy
import os
import pytoml as toml


class Searcher:
    """
    Generate config.toml and create inverted index.
    Wraps the MeTA search engine and its rankers.
    """
    def __init__(self, author, ds_name, path):
        """
        Create/load a MeTA inverted index based on the provided config file and
        set the default ranking algorithm to Okapi BM25.
        :param author: author name of dataset
        :param ds_name: dataset name
        :param path: path to dataset (data/author), append ds_name to get full path
        """
        print(author)
        print(ds_name)
        print(path)
        self.default_ranker = metapy.index.OkapiBM25()
        cfg = self.generate_config(author, ds_name, path)
        cwd = os.getcwd()
        os.chdir(path)
        self.idx = metapy.index.make_inverted_index(cfg)
        os.chdir(cwd)

    def search(self, query, ranker_name, params={}, num_results=5):
        """
        Accept a query and a ranker and run the provided query with the specified
        ranker.
        :param query: string of query
        :param ranker_name: name of the ranker to be used
        :param params: dict of arguments to be passed into ranker (mutable, do not change)
        :param num_results: return top k relevant documents (k = 5 by default)
        :return: dict of response
        """
        start = time.time()
        q = metapy.index.Document()
        q.content(query)
        try:
            ranker_cls = getattr(metapy.index, ranker_name)
            for key in params:
                setattr(ranker_cls, str(key), float(params[key]))
            ranker = ranker_cls()
        except Exception as e:
            print("Couldn't make '{}' ranker, using default.".format(ranker_name))
            ranker = self.default_ranker
        response = {'query': query, 'results': []}
        for result in ranker.score(self.idx, q, num_results):
            response['results'].append({
                'score': float(result[1]),
                'doc_id': result[0],
                'name': self.idx.doc_name(result[0]),
                'path': self.idx.doc_path(result[0])
            })
        response['elapsed_time'] = time.time() - start
        return response

    @staticmethod
    def generate_config(author, ds_name, path):
        """
        Construct config.toml for the dataset &
        Assume line.toml is constructed after uploading
        If already exists, return the config file
        """
        cfg = path + "/" + ds_name + "-config.toml"
        if os.path.isfile(cfg):
            return cfg
        obj = dict()
        obj['prefix'] = "."
        obj['dataset'] = ds_name
        obj['corpus'] = "line.toml"
        obj['index'] = ds_name+"-idx"
        obj['analyzers'] = [dict()]
        analyzer = obj['analyzers'][0]
        analyzer['ngram'] = 1
        analyzer['method'] = "ngram-word"
        analyzer['filter'] = [{'type': "icu-tokenizer"}, {'type': "lowercase"}]
        with open(cfg, 'w+') as f:
            toml.dump(f, obj)
        return cfg
