from __future__ import generators
import os
import string
import sys
import time


from Node import Node
from Node import nodesFromPath

class NodeProxy:
    def __init__(self, filename, data, typ):
        self._filename = filename
        self._data = data
        self._type = typ

    def filename(self):
        return self._filename
    def type(self):
        return self._type

    def replace(self):
        try:
            obj = Node(self._filename,self._data)
        except:
            raise AttributeError("Couldn't load node:"+self._filename)
        self.__dict__ = obj.__dict__
        self.__class__ = obj.__class__
	return

    def __getattr__(self, name):
        if name == "filename":
            return self._filename
        self.replace()
        return getattr(self, name)

    def __setattr__(self, name, value):
        if name in [ '_filename', '_type', '_data' ]:
            self.__dict__[ name ] = value

        else:
            self.replace()
            setattr(self, name, value)


def sortChronological(l):
    def sorter(a,b):
        return cmp(time.mktime(a.date),time.mktime(b.date))
    l.sort(sorter)
    return l

class _NodeFactory:

    def __init__(self,base='/home/mike/projects/mike-warren.com/content'):
        self._nodes = []
        
        self.directory(base)
        self.postprocess()


    def append(self,nodeorproxy):
        self._nodes.append(nodeorproxy)


    def postprocess(self):
        for node in self.nodes():
            node.postprocess(self)

    def nodes(self):
        return self._nodes
    def nodesByType(self,typ):
        rtn = []
        for x in self._nodes:
            if not hasattr(x,"type"):
                print "no type:",x
            elif x.type() == typ:
                rtn.append(x)
        return rtn

    def articles(self):
        return NodeFactory.nodesByType('article')
    def movies(self):
        return NodeFactory.nodesByType('movie')
    def links(self):
        return NodeFactory.nodesByType('link')
    def topics(self):
        return NodeFactory.nodesByType('topic')
    def messages(self):
        return NodeFactory.nodesByType('message')

    def nodeFromTitle(self,title):
        title = title.strip().lower()
        for node in self.nodes():
            if node.title.strip().lower() == title:
                return node
        return None


    def directory(self,directory):
        all = os.listdir(directory)
        for file in all:
            path = os.path.join(directory,file)
            if os.path.isfile(path):
                if file[-4:] == 'sgml':
                    n = nodesFromPath(path)
                    self._nodes = self._nodes + n
                    sys.stderr.write( '\b\b\b\b\b%05d' % len(self._nodes) )
                    sys.stderr.flush()

            else:
                self.directory(os.path.join(directory,file))


sys.stderr.write( "loading 00000" )
sys.stderr.flush()
NodeFactory = _NodeFactory()
sys.stderr.write( " nodes.\n" )
