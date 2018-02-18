from collections import namedtuple
from itertools import count

PinName = namedtuple('PinName', 'numeric full')
ModAttr = namedtuple('ModAttr', 'type value')

ModPin = namedtuple('ModPin', 'module pinnum')
ModCall = namedtuple('ModCall', 'factname args')

class NodeManager():
    def __init__(self):
        self.nodes = dict()
        self.anon_node_iterator = count()
    
    def make(self, name=None):
        # create anonymous node
        if name == None:
            name = "anon" + str(next(self.anon_node_iterator))
            node = Node(name = name)
        else:
            node = Node(name = name, anon=False)
        
        if name in self.nodes:
            raise Exception("Duplicate node name!")

        self.nodes[name] = node
        return node
    
    def get_node(self, name):
        if name in self.nodes:
            return self.nodes[name]
        else:
            return None

class ModManager():
    def __init__(self):
        self.mod_factories = dict()
        self.mods = dict()
        self.anon_iterator = count()
        
    def add_factory(self, factory):
        self.mod_factories[factory.name] = factory
    
    def make_mod(self, factname, modname=None):
        if factname in self.mod_factories:
            mod = self.mod_factories[factname].make()
            if modname == None:
                modname = "anon" + str(next(anon_iterator))
            self.mods[modname] = mod
            return mod
        return None
    
    def get_mod(self, modname):
        if modname in self.mods:
            return self.mods[modname]
        
                

class Node():
    def __init__(self, name=None, anon=True):
        self.name = name
        self.anon = anon
        self.master = None
        self.slaves = []
        self.pins = []
    
    def connect_pin(self, module, pinnum):
        prev_node = module.get_node(pinnum)
        
        if prev_node != None:
            self.combine_node(prev_node)
        else:
            module.set_node(pinnum, self)
            self.pins.append((module, pinnum))
    
    def combine_node(self, node):
        
        node_m = node.get_master()
        self_m = self.get_master()
        
        # this node is anon, and the other node is named
        if self_m.anon and not node_m.anon:
            master_node = node_m
            slave_node = self_m
        # this node is master
        else: 
            master_node = self_m
            slave_node = node_m
        
        # redirect all pins from slave
        for (mod, pn) in slave_node.pins:
            mod.set_node(pn, master_node)
            master_node.pins.append((mod, pn))
        slave_node.pins = []
        
        
        master_node.slaves.append(slave_node)
        slave_node.master = master_node
        
        # update slaves of the slave to point to master
        for s in slave_node.slaves:
            assert(len(s.pins) == 0)
            master_node.slaves.append(s)
            s.master = master_node
        
        
    def get_master(self):
        if self.master == None:
            return self
        else:
            return self.master.get_master()

    def __repr__(self):
        return f"Node('{self.name}')"
        

class ModuleFactory():
    
    def __init__(self, name, args, attrs):
        self.name = name
        self._args = args
        self._attrs = attrs
        
        self._pnum = 0
        self._pins = PinName([], [])
        
        for a in self._attrs:
            if type(a) == ModAttr:
                if a.type == 'pins':
                    self._pnum = len(a.value)
                    self._pinnames = a.value
                    
                    self._pindict_numeric = dict()
                    self._pindict_full = dict()
                    for i, (pn, pf) in enumerate(self._pinnames):
                        if not pn in self._pindict_numeric:
                            self._pindict_numeric[pn] = i
                        else:
                            raise Exception("Duplicate Numeric Node Name!")
                        
                        if pf != 'NC' and not pf in self._pindict_numeric:
                            self._pindict_full[pf] = i
                        elif pf != 'NC':
                            raise Exception("Duplicate Full Node Name!")
    
    def make(self):
        return Module(self.name, self._args, self._pnum, self._pinnames, self._pindict_numeric, self._pindict_full)
    


        
class Module():
    # TODO create class methods and factory should just directly access
    # class variables
    def __init__(self, name, args, pnum, pinnames, pd_num, pd_full):
        self._name = name
        self._args = args
        self._pnum = pnum
        self._pinnames = pinnames
        self._pd_num = pd_num
        self._pd_full = pd_full
    
        self._pin_nodes = [None] * self._pnum
        
    def ref_to_pinnum(self, ref, reftype):
        if reftype == 'full':
            pinnum = self._pd_full[ref]
        elif reftype == 'numeric':
            pinnum = self._pd_num[ref]
        elif reftype == 'index':
            pinnum = int(ref)
        
        return pinnum
        
    def connect_node(self, pinnum, node):
        
        node.connect_pin(self, pinnum)

    def get_node(self, pinnum):
        return self._pin_nodes[pinnum]
    
    def set_node(self, pinnum, node):
        self._pin_nodes[pinnum] = node
    
        
    
                    
    
        
