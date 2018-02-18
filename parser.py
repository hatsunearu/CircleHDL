#!/bin/env python3

from lark import Lark, Transformer
from pprint import pprint


from circle import *


class CircleTransformer(Transformer):
    
    def __init__(self, node_manager, mod_manager):
        self.nm = node_manager
        self.mm = mod_manager
        
    def definition(self, items):
        return items
        
    def moddef(self, items):
        
        mod_name = items[0].value
        mod_args = items[1]
        mod_attrs = items[2]
        
        print(f"mod_name: {mod_name}\nmod_args: {mod_args}\nmod_attrs: {mod_attrs}")
        
        mf = ModuleFactory(mod_name, mod_args, mod_attrs)
        
        self.mm.add_factory(mf)
        
        return mf
    
    def moddef_body(self, items):
        return items
        
    def functional_args(self, items):
        return items
        
    def attr_pins(self, items):
        num_pins = items[0].value
        pinname_stmts = items[1]
        
        assert(len(pinname_stmts) == int(num_pins)) # for now
        
        return ModAttr('pins', pinname_stmts)
        
    def pins_body(self, items):
        return items
    
    def pinname_stmt(self, items):
        return PinName(items[0].value, items[1].value)
        
    def call_mod(self, items):
        factname = items[0].value
        args = items[1]
        return ModCall(factname, args)
    
    def decl_mod(self, items):
        modname = items[0].value
        factname, args = items[1]
        
        self.mm.make_mod(factname, modname)
    
    def decl_node(self, items):
        # todo check dupes
        nodename = items[0].value
        self.nm.make(nodename)
        
    def double_port(self, items):
        # items can be a tuple of length 1, 2
        # 1: a single port to be connected up to the parent node
        # 2: left-right port pair from module
        
        # additionally, it can be a list of length-2 tuples
        # which are the two left-right port pair from the child modules
        pass

    def singular_port(self, items):
        return (items[0],)
    
    def node_literal(self, items):
        lit = items[0].value
        # check existance of node
        node = self.nm.get_node(lit)

    def mod_literal(self, items):
        lit = items[0].value
        # check existance of mod
        mod = self.nm.get_mod(lit)
    
    def functional_args(self, items):
        return [i.value for i in items]
    
    def mod_pin_full(self, items):
        # TODO add checks
        modname = items[0].value
        pinname = items[1].value
        mod = self.mm.get_mod(modname)
        pinnum = mod.ref_to_pinnum(pinname, 'full')
        
        node_on_pin = mod.get_node(pinnum)
        
        if node_on_pin != None:
            node = self.nm.make()
            node.connect_pin(mod, pinnum)
            node_on_pin = node
          
        return node_on_pin
    
        




g = open('circle.g').read()

circle_parser = Lark(g, start='top')

res = circle_parser.parse(open("mod.circ").read())
print(res.pretty())


nm = NodeManager()
mm = ModManager()

xfrm = CircleTransformer(nm, mm).transform(res)

modulefactories = [mf for mf in xfrm.children if type(mf) == ModuleFactory]

print(modulefactories)

m = modulefactories[0].make()
n1 = Node('n1')
n2 = Node('n2', anon=False)
n3 = Node('n3', anon=False)

n1.connect_pin(m, 2)
n2.connect_pin(m, 3)
n3.connect_pin(m, 2)
n1.connect_pin(m, 3)

print(f"4:\nn1: {n1.pins} n2: {n2.pins} n3: {n3.pins}")
print(f"m pn: {m._pin_nodes}")



print()




