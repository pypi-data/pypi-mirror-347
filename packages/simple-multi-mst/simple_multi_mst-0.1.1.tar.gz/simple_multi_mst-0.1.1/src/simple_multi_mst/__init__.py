import json
import numpy as np
import pandas as pd
import random
from scipy.spatial.distance import pdist, squareform
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from returns.pipeline import flow

class MultiMST:
    def __init__(self, df, cols=[], metric='euclidean', max_amount=0, iterations=10):
        self.df = df
        self.cols = cols
        self.metric = metric
        self.max_amount = max_amount
        self.iterations = iterations
        self.links = []
        if 'id' not in self.df.columns:
            self.df.insert(0, 'id', range(0, len(self.df)))
    
    def add_mst_to_links(self, mst):
        for i in range(0,len(mst[0])):
            self.links.append([mst[0][i], mst[1][i]])
        # remove duplicates
        self.links = list(set(tuple(link) for link in self.links))
        return self.links

    def create_links(self, distances):
        for _ in range(self.iterations):
            flow(distances, 
                lambda d: alter_distances(d, max_amount=self.max_amount),
                lambda d: calculate_mst(d),
                lambda d: self.add_mst_to_links(d))

    def run(self):
        distances = calculate_distances(self.df, self.cols, self.metric)
        self.create_links(distances)
        return to_json(self.df, self.links)
    
    def export(self, format="json", base_filename="output"):
        if format == "json":
            links_as_json = [{'source': int(item[0]), 'target': int(item[1])} for item in self.links]
            nodes_as_json = self.df.to_dict(orient="records")

            graph = {'nodes': nodes_as_json, 'links': links_as_json}
            with open(f"{base_filename}.json", "w") as _f:
                json.dump(graph, _f)
        elif format == "csv":
            self.df.to_csv(f"{base_filename}_nodes.csv", index=False)
            _links_df = pd.DataFrame(self.links, columns=['source', 'target'])
            _links_df.to_csv(f"{base_filename}_links.csv", index=False)
    
def calculate_distances(df,cols=[],metric='euclidean'):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    if len(cols) == 0:
        cols = df.columns.tolist()
    if 'id' in cols:
        cols.remove('id')
    distances = pdist(df[cols], metric=metric)
    distance_matrix = squareform(distances)
    return distance_matrix

def nodes(df):
    return df.to_dict(orient="records")

def alter_distances(distances, max_amount=0):
    if max_amount == 0:
        max_amount=np.std(distances) / 50
    changer = lambda t: t + random.uniform(0, max_amount)
    return np.array([changer(d) for d in distances])

def calculate_mst(distances):
    X = csr_matrix(distances)
    mst = minimum_spanning_tree(X)
    return np.nonzero(mst)

def to_json(df, links):
    links_as_json = [{'source': int(item[0]), 'target': int(item[1])} for item in links]
    nodes_as_json = df.to_dict(orient="records")
    return {'nodes': nodes_as_json, 'links': links_as_json}