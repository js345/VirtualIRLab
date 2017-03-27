from unittest import TestCase
from search.searcher import Searcher
import pytoml as toml
import os
import shutil


class TestSearcher(TestCase):

    def setUp(self):
        self.author = "test"
        self.path = os.getcwd() + "/data/" + self.author
        self.ds_name = "cranfield"
        self.searcher = Searcher(author=self.author, ds_name=self.ds_name, path=self.path)

    def tearDown(self):
        os.remove(self.path+"/"+self.ds_name+"-config.toml")
        shutil.rmtree(self.path+"/"+self.ds_name+"-idx")
        self.author = ""
        self.path = ""
        self.ds_name = ""

    def test_search(self):
        query = "experimental investigation of the aerodynamics of a wing in a slipstream"
        ranker_name = "OkapiBM25"
        self.searcher.search(query, ranker_name)

    def test_generate_config(self):
        cfg = Searcher.generate_config(self.author, self.ds_name, self.path)
        with open(cfg, 'rb') as fin:
            obj2 = toml.load(fin)
        obj1 = dict()
        obj1['prefix'] = "."
        obj1['dataset'] = self.ds_name
        obj1['corpus'] = "line.toml"
        obj1['index'] = self.ds_name + "-idx"
        obj1['analyzers'] = [dict()]
        analyzer = obj1['analyzers'][0]
        analyzer['ngram'] = 1
        analyzer['method'] = "ngram-word"
        analyzer['filter'] = [{'type': "icu-tokenizer"}, {'type': "lowercase"}]
        self.assertDictEqual(obj1, obj2, "Config generation error")
