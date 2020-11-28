from typing import List 

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

class WriteMemoryBlock(MemoryBlock):
    def __init__(self, label : str, rhs : List[str],  writeLine : bool, isVariable = False, memory = None):
        MemoryBlock.__init__(self, label)
        self.rhs = rhs
        self.writeLine = writeLine
        self.isVariable = isVariable
        self.memory = memory

    def run(self, pc : int):
        if self.isVariable:
            oldvar = self.rhs 
            # Find variable in memory and grab value
            for memblock in self.memory.items:
                if type(memblock) == AssignmentMemoryBlock:
                    if str(memblock.lhs) == str(self.rhs[0]):
                        self.rhs[0] = memblock.rhs
                        break
            if str(self.rhs[0]) == str(oldvar):
                # Error 
                print("Error: variable not found")
                print(self.memory.items)
                print(1/0)
                return pc + 1

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
