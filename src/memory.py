from __future__ import annotations
from typing import List, Tuple
import sys 
class Memory():
    def __init__(self, items : List[MemoryBlock]=[], pc : int=0):
        """Initializes a memory object with a list of memory blocks and a program counter

        Args:
            items (List, optional): A list of memory blocks Defaults to [].
            pc (int, optional): A program counter. Defaults to 0.
        """
        self.pc = pc
        self.items = items 

    def increasePC(self) -> Memory:
        """Returns a memory object with the same items, but an increased program counter

        Returns:
            Memory: A memory object with an increased program counter
        """
        return Memory(self.items, self.pc + 1)

    def push(self, item : MemoryBlock) -> Memory:
        """Returns a memory object with the same 

        Args:
            item (MemoryBlock): A memory block to add to the memory object

        Returns:
            Memory: A memory object with the added memory block
        """
        return Memory(self.items + [item], self.pc)

    def pop(self) -> Tuple(MemoryBlock, Memory):
        """Returns the item at the top of memory and return the remaining memory

        Returns:
            Tuple(MemoryBlock, Memory): The item at the top of the memory and a memory object with the remaining memory
        """
        return (self.item[-1], Memory(self.items[:-1], self.pc))

    def run(self) -> Memory:
        """Runs a memory block in memory

        Returns:
            Memory: A memory object without the previously ran memory block
        """
        if self.pc >= len(self.items):
            return None
        newpc = self.items[self.pc].run(self.pc) # Run the function in current memory block
        return Memory(self.items, newpc) # Return a new memory with(possibly) increased pc 



class MemoryBlock():
    def __init__(self, label : str):
        """Initializes a memory block with the given label

        Args:
            label (str): The label to give to the memory block
        """
        self.label = label # Label is the name in assembly. For a function the name + params, or in a location statement

    def run(self, pc : int) -> int:
        """Runs the current memory block

        Args:
            pc (int): The current program counter

        Returns:
            int: The program counter after the memory block has run
        """
        return pc+1

class LocationMemoryBlock(MemoryBlock):
    def run(self, pc : int):
        """Runs the location memory block

        Args:
            pc (int): The current program counter

        Returns:
            int: The program counter after the memory block has run
        """
        return pc+1

def findVar(memory : Memory, name : str) -> str:
    """Attempts to find the value of a variable in the current memory block

    Args:
        memory (Memory): The memory
        name (str): The variable's identifier

    Returns:
        str: Returns either the variable's value or the identifier if it's not found
    """

    oldvar = name
    # todo: no for
    for memblock in memory.items:
         if type(memblock) == AssignmentMemoryBlock:
                if str(memblock.lhs) == str(name):
                    name = memblock.rhs
                    return name 
    if oldvar == name:
        print("Error: var not found")
        print(1/0)
        return name
    
def runWrite(word : str, rhs : List[str]):
    print(word, end="")
    if rhs.index(word) != len(rhs)-1:
        print(" ", end="")


class WriteMemoryBlock(MemoryBlock):
    def __init__(self, label : str, rhs : List[str],  writeLine : bool, isVariable = False, memory = None):
        """Initializes a write memory block

        Args:
            label (str): The memory block's label
            rhs (List[str]): What to write
            writeLine (bool): Whether or not to write a new line
            isVariable (bool, optional): If the rhs is a variable or just a plain string. Defaults to False.
            memory ([type], optional): The memory. Required when a variable is passed, so it can be found. Defaults to None.
        """
        MemoryBlock.__init__(self, label)
        self.rhs = rhs
        self.writeLine = writeLine
        self.isVariable = isVariable
        self.memory = memory

    def run(self, pc : int) -> int:
        """Runs the write memory block

        Args:
            pc (int): The current program counter

        Returns:
            int: The program counter after the memory block has ran
        """
        if self.isVariable:
            # Find variable in memory and grab value
            findVar(self.memory, self.rhs[0])
            
        result = list( map(lambda word: runWrite(word, self.rhs), self.rhs) )
            
        if self.writeLine:
            print("\n", end="")
        return pc+1

class GotoMemoryBlock(MemoryBlock):
    def __init__(self, label: str, rhs : str, memory : Memory):
        """Initializes a goto memory block

        Args:
            label (str): The memory's label
            rhs (str): The label to jump to
            memory (Memory): The memory(to find the label to jump to)
        """
        MemoryBlock.__init__(self, label)
        self.rhs = rhs 
        self.memory = memory
    #todo: recusrive
    def run(self, pc : int) -> int:
        """Runs the goto memory block

        Args:
            pc (int): The current program counter

        Returns:
            int:  The program counter after the memory block has ran
        """
        for memblock in self.memory.items:
            if memblock.label == self.rhs: 
                return self.memory.items.index(memblock)
        
class AssignmentMemoryBlock(MemoryBlock):
    def __init__(self, label: str, lhs: str, rhs : str, asstype : str):
        """Initializes an assignment memory block

        Args:
            label (str): The memory's Label
            lhs (str): The assignment's name 
            rhs (str): The assignment's value
            asstype (str): The assignment's type
        """
        MemoryBlock.__init__(self, label)
        self.lhs = lhs 
        self.rhs = rhs 
        self.asstype = asstype 

    def run(self, pc : int) -> int:
        """Runs the assignment memory bock

        Args:
            pc (int): The current program counter

        Returns:
            int: The program counter after the memory block ran
        """
        return pc + 1

class IfMemoryBlock(MemoryBlock):
    def __init__(self, label : str, lhs : str, rhs : str, compare_operator : str, memory : Memory):
        """Initializes an if memory block

        Args:
            label (str): The memory block's label
            lhs (str): The left variable to check
            rhs (str): The right variable to check
            compare_operator (str): What operator to use for the check, i.e. ==
            memory (Memory)): The memory
        """
        MemoryBlock.__init__(self, label)
        self.lhs = lhs 
        self.rhs = rhs 
        self.compare_operator = compare_operator
        self.memory = memory 

    def run(self, pc : int) -> int:
        """Runs the if memory block

        Args:
            pc (int): The current program counter

        Returns:
            int: The program counter after the if statement
        """
        if self.compare_operator == '==':
            if findVar(self.memory, self.lhs) == findVar(self.memory, self.rhs):
                # print(self.memory.items)
                return pc + 1

        return pc+2

class ExitMemoryBlock(MemoryBlock):
    def run(self, pc : int):
        """Runs the exit memory block

        Args:
            pc (int): The current program counter
        """
        sys.exit(0)