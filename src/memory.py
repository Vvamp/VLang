from typing import List 
import sys 
class Memory():
    def __init__(self, items=[], pc=0):
        self.pc = pc
        self.items = items 

    def increasePC(self):
        return Memory(self.items, self.pc + 1)

    def push(self, item):
        return Memory(self.items + [item])

    def pop(self):
        """Returns the item at the top of memory and return the remaining memory

        Returns:
            Tuple(): [description]
        """
        return (self.item[-1], Memory(self.items[:-1], self.pc))

    def run(self):
        """Run the program in memory 
        """
        if self.pc >= len(self.items):
            return None
        newpc = self.items[self.pc].run(self.pc) # Run the function in current memory block
        return Memory(self.items, newpc) # Return a new memory with(possibly) increased pc 



class MemoryBlock():
    def __init__(self, label : str):
        self.label = label # Label is the name in assembly. For a function the name + params, or in a location statement

    def run(self, pc : int):
        return pc+1

class LocationMemoryBlock(MemoryBlock):
    def run(self, pc : int):
        return pc+1

def findVar(memory, name):
    oldvar = name
    for memblock in memory.items:
         if type(memblock) == AssignmentMemoryBlock:
                if str(memblock.lhs) == str(name):
                    name = memblock.rhs
                    return name 
    if oldvar == name:
        print("Error: var not found")
        print(1/0)
        return name
    

class WriteMemoryBlock(MemoryBlock):
    def __init__(self, label : str, rhs : List[str],  writeLine : bool, isVariable = False, memory = None):
        MemoryBlock.__init__(self, label)
        self.rhs = rhs
        self.writeLine = writeLine
        self.isVariable = isVariable
        self.memory = memory

    def run(self, pc : int):
        if self.isVariable:
            # Find variable in memory and grab value
            findVar(self.memory, self.rhs[0])

        for word in self.rhs:
            print(word, end="")
            if self.rhs.index(word) != len(self.rhs)-1:
                print(" ", end="")
        if self.writeLine:
            print("\n", end="")
        return pc+1

class GotoMemoryBlock(MemoryBlock):
    def __init__(self, label: str, rhs : str, memory : Memory):
        MemoryBlock.__init__(self, label)
        self.rhs = rhs 
        self.memory = memory

    def run(self, pc : int):
        for memblock in self.memory.items:
            if memblock.label == self.rhs: 
                return self.memory.items.index(memblock)
        
class AssignmentMemoryBlock(MemoryBlock):
    def __init__(self, label: str, lhs, rhs : str, asstype : str):
        MemoryBlock.__init__(self, label)
        self.lhs = lhs 
        self.rhs = rhs 
        self.asstype = asstype 

    def run(self, pc : int):
        return pc + 1

class IfMemoryBlock(MemoryBlock):
    def __init__(self, label : str, lhs, rhs, compare_operator, memory):
        MemoryBlock.__init__(self, label)
        self.lhs = lhs 
        self.rhs = rhs 
        self.compare_operator = compare_operator
        self.memory = memory 

    def run(self, pc : int):
        if self.compare_operator == '==':
            if findVar(self.memory, self.lhs) == findVar(self.memory, self.rhs):
                print(self.memory.items)
                return pc + 1

        return pc+2

class ExitMemoryBlock(MemoryBlock):
    def run(self, pc : int):
        sys.exit(0)