import urllib
from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class DBpediaWrapperConfig:
    es_host: str = 'localhost'
    index: str = 'dbpedia'
    sparql_endpoint: str = 'http://dbpedia.org/sparql'
    default_graph: str = 'http://dbpedia.org'


class Entity(NamedTuple):
    uri: str

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Entity):
            return urllib.parse.unquote(self.uri).lower() == urllib.parse.unquote(o.uri).lower()
        return False


class Class(NamedTuple):
    uri: str


class Property(NamedTuple):
    uri: str