import re
from typing import Optional, Union
import rdflib.namespace
from rdflib.namespace import Namespace, OWL, RDF, XSD
from rdflib import URIRef
import warnings
from kgtk.exceptions import WrongFormatURIException, PrefixNotFoundException, PrefixAlreadyUsedException
from kgtk.exceptions import SplitURIWithUnknownPrefix
from kgtk.knowledge_graph.node import URI


SCHEMA = Namespace('http://schema.org/')
DIG = Namespace('http://dig.isi.edu/ontologies/dig/')

URI_PATTERN = re.compile(r'^http:|^urn:|^info:|^ftp:|^https:')
URI_ABBR_PATTERN = re.compile(r'^(?:([^:]*):)?([^:]+)$')


class NamespaceManager(rdflib.namespace.NamespaceManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph.namespace_manager = self

    def parse_uri(self, text: Union[str, URI]) -> URIRef:
        """
        Parse input text into URI

        :param text: can be one of
              1. URI, directly return
              2. prefix:name, query namespace for prefix, return expanded URI
              3. name, use default namespace to expand it and return it
        :return: URIRef
        """
        if self.check_uriref(text):
            return self.check_uriref(text)
        elif isinstance(text, str):
            text = text.strip()
            m = URI_ABBR_PATTERN.match(text)
            if m:
                prefix, name = m.groups()
                base = self.store.namespace(prefix if prefix else '')
                if not base:
                    raise PrefixNotFoundException("Prefix: %s", prefix)
                return URIRef(base + name)
        elif isinstance(text, URI):
            return self.parse_uri(text.value)
        raise WrongFormatURIException(text)

    def bind(self, prefix: str, namespace: str, override=True, replace=True):
        """
        bind a given namespace to the prefix, forbids same prefix with different namespace

        :param prefix:
        :param namespace:
        :param override: if override, rebind, even if the given namespace is already bound to another prefix.
        :param replace: if replace, replace any existing prefix with the new namespace
        """
        namespace = URIRef(str(namespace))
        # When documenting explain that override only applies in what cases
        if prefix is None:
            prefix = ''
        bound_namespace = self.store.namespace(prefix)
        # Check if the bound_namespace contains a URI and if so convert it into a URIRef for
        # comparison. This is to prevent duplicate namespaces with the same URI.
        if bound_namespace:
            bound_namespace = URIRef(bound_namespace)
        if bound_namespace and bound_namespace != namespace:

            # prefix already in use for different namespace
            if replace:
                self.store.bind(prefix, namespace)
            else:
                warnings.warn("Prefix ({}, {}) already defined, if want to replace it, set flag replace to True".format(
                    prefix if prefix else None, self.store.namespace(prefix)))
        else:
            bound_prefix = self.store.prefix(namespace)
            if bound_prefix is None:
                self.store.bind(prefix, namespace)
            elif bound_prefix == prefix:
                pass  # already bound
            else:
                if override or bound_prefix.startswith("_"):
                    self.store.bind(prefix, namespace)

    @staticmethod
    def check_uriref(text: Union[str, URI]) -> Optional[URIRef]:
        """
        Check if the input text is likely to be an URIRef and return None or URIRef
        """
        if isinstance(text, URIRef):
            return text
        if isinstance(text, URI):
            text = text.value
        if isinstance(text, str):
            text = text.strip()
            if URI_PATTERN.match(text.strip()):
                return URIRef(text)

    def split_uri(self, uri: str):
        """
        Overwrite rdflib's implementation which has a lot of issues
        """
        ns = ''
        for prefix, namespace in self.store.namespaces():
            if uri.startswith(namespace) and len(namespace) > len(ns):
                ns = namespace
        if ns:
            return ns, uri[len(ns):]
        raise SplitURIWithUnknownPrefix()

    def bind_for_master_config(self):
        """
        Bind must-have namespaces for master config, note RDF and XSD are already bound
        """
        self.bind('owl', OWL)
        self.bind('', 'http://isi.edu/default-ns/')

    def compute_qname(self, uri, generate=True):
        namespace, name = self.split_uri(uri)
        namespace = URIRef(namespace)
        prefix = self.store.prefix(namespace)
        if prefix is None:
            if not generate:
                raise Exception("No known prefix for %s and generate=False")
            num = 1
            while 1:
                prefix = "ns%s" % num
                if not self.store.namespace(prefix):
                    break
                num += 1
            self.bind(prefix, namespace)
        return prefix, namespace, name


if __name__ == '__main__':
    from rdflib import Graph
    nm = NamespaceManager(Graph())
    nm.bind('wdref', 'http://www.wikidata.org/reference/')
    print(nm.split_uri('http://www.wikidata.org/reference/355b56329b78db22be549dec34f2570ca61ca056'))
    print(nm.compute_qname('http://www.wikidata.org/reference/355b56329b78db22be549dec34f2570ca61ca056'))
