import requests
import logging
import os
from typing import Any
from collections.abc import Callable
import networkx as nx

import pandas as pd

class WDCException(Exception):
    def __init__(self, message, query = None, state = None):
        super().__init__(message)
        self.query = query
        self.state = state;
        
    def __str__(self):
        return (
            super().__str__() +
            ", query: " + self.query + 
            ", state: " + self.state)

class WDCClient: 
    
    @staticmethod
    def fromEnv():
        """Create a WDCClient from the 'Environment'
        
        Uses the environment variables 'WDC_HOST' and 'WDC_TOKEN' from the current
        environment. Thus you can make use of modules such as python-dotenv
        or other variants more easily.
        
        Remember: Using passwords or tokens in source code is dangerous!
        """
        _host = os.getenv('WDC_HOST')
        _token = os.getenv('WDC_TOKEN')
        
        client = WDCClient(host = _host, token = _token)
        
        return client

    def __init__(self, host: str, token = None):
        self.logger = logging.getLogger(__name__)
        self.host = host 
        self.token = token
        
        if self.host == None:
            raise WDCException("Could not create WDCClient with host = None")
        
        self.session = requests.Session()
        if self.token != None: 
            self.session.headers.update({'token': self.token})

        
    def loadAsDataFrame(self, endpoint: str, params: dict[str, Any] = {}) -> pd.DataFrame: 
        json = self.loadAsJson(endpoint, params);
        
        return pd.json_normalize(json)
        
    def loadForEach(self, endpoint: str, params: dict[str, Any] = {}, f: Callable[[Any, int, int], None] = None) -> None:
        url = self.host + "/" + endpoint
        
        self.logger.debug('endpoint:' + url + ', params:' + str(params))
        
        counter = 1
        while url != None: 
            response = self.session.get(url, params = params)
            self.logger.debug("headers: %s", response.headers)
    
            json = response.json()
            
            # Everything ok? 
            if json['responseHeader']['state'] != 'OK':
                raise WDCException(
                    json['responseHeader']['msg'], 
                    query = json['responseHeader']['query'], 
                    state = json['responseHeader']['state'])
            
            self.logger.debug("json: %s", json)
            
            for e in json["content"]:
                f(e, counter, json['page']['totalElements'])
                counter += 1
            
            # gehts weiter?
            if 'links' in json and 'next' in json['links']:
                url = json['links']['next']
                self.logger.debug("nextLink %s", url)
            else: 
                url = None
        
    def loadAsJson(self, endpoint: str, params: dict[str, Any] = {}) -> []: 
        res = []
        
        def collect_it(e, pos, maxPos):
            nonlocal res
            res.append(e)
            
        self.loadForEach(endpoint, params, collect_it)
        
        return res
    
    def __str__(self) -> str:
        return "[host=" + str(self.host) + ", token=" + str(self.token) + "}"
    
    def loadDomainGraph(self, snapshot: str, selection: str = None, variant = 'ONLY_SEEDS'):
        """
        Loads a DomainGraph as a NetworkX-Graph (DiGraph). 
        
        Args:
            snapshot: The machineName of the snapshot.
            selection: A selection of the snapshot.
            variant: A value of an enumeration of the variant of the DomainGraph.
            
        Returns: 
            : DiGraph of the DomainGraph
        """
        domainGraphs = self.loadAsJson(
            f"/api/domaingraph/list", 
            { 
                "snapshot": snapshot, 
                "selection": selection, 
                "variant": variant
            })
        
        self.logger.debug("domainGraphs:" + str(domainGraphs))
        
        # es darf nur einer sein
        if len(domainGraphs) != 1: 
            raise WDCException("There must be exactly one DomainGraph but found: " + len(domainGraphs))
        
        domainGraphId = domainGraphs[0]['id']
        
        # Graph bauen
        graph = nx.DiGraph()
        for n in self.loadAsJson(f"/api/domaingraph/{domainGraphId}/nodes"):
            _id = n.pop("id")
            graph.add_node(_id, **n)
            
        for e in self.loadAsJson(f"/api/domaingraph/{domainGraphId}/edges"):
            graph.add_edge(e['source'], e['target'], weight=e['weight'])
        
        return graph

    