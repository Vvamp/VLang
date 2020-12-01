from __future__ import annotations
from typing import List, Tuple, Union
import sys 

def modvar(item : LookUpItem, name : str, value, items : List[LookUpItem]) -> Union[None, LookUpTable]:
    """Modifies a variable with the given value

    Args:
        item (LookUpItem): The current item to possibly modify 
        name (str): The name of the variable to modify
        value ([type]): The value to set the variable to 
        items (List[LookUpItem]): The list of all items that can possibly be the variable the modify

    Returns:
        Union[None, LookUpTable]: If the variable exists, return a new table with the modified variable. If it does not exist, return None
    """
    if item.name == name:
        index = items.index(item)

        upperbound = index+1

        items_without_mod = items[:index] + items[upperbound:]
        table_without_mod = LookUpTable(items_without_mod)
        table_with_mod = table_without_mod.addVariable(name, value)
        return table_with_mod
    else: 
        return None


def findLabel(memblock : MemoryBlock, name : str, memory : Memory) -> str:
    """Checks if a memory block has a label and return the index of it

    Args:
        memblock (MemoryBlock): The memory block to find the index of
        name (str): The name to find
        memory (Memory): The memory to look in

    Returns:
        str: [description]
    """
    if memblock.label == name:
        return memory.items.index(memblock)

def findFirstVar(results : List[Union[None, int]]) -> Union[None, int]:
    """Finds the first index in a list of none's

    Args:
        results (List[Union[None, int]]): A list of none's and integers

    Returns(either):
        int: The first item's value(index)
        None: If there were no indexes in the list, return none
    """
    if len(results) == 0:
        return None 
    if results[0] is not None:
        return results[0]
    return findFirstVar(results[1:])

def runWrite(word : str, rhs : List[str]):
    """Writes a word to the terminal and if it's not the last word in the rhs, write a space

    Args:
        word (str): [description]
        rhs (List[str]): [description]
    """
    print(word, end="")
    if rhs.index(word) != len(rhs)-1:
        print(" ", end="")

class LookUpTable():
    def __init__(self, items : List[LookUpItem]= []):
        """Initializes a variable lookup table

        Args:
            items (List[LookUpItem], optional): A list of variables(look up item). Defaults to [].
        """
        self.items = items 
    
    def addVariable(self, item : LookUpItem) -> LookUpTable:
        """Return a new LookUpTable with the given lookUpItem added 

        Args:
            item (LookUpItem): The item to add

        Returns:
            LookUpTable: The new table with the item
        """
        return LookUpTable(self.items + [item])

    def addVariable(self, name : str, value) -> LookUpTable:
        """Create a new lookup item and return a new table with the created item

        Args:
            name (str): The item's name
            value ([type]): The value of that item

        Returns:
            LookUpTable: The new lookup table with the added item
        """
        # Check if variable exists 
        result = self.modVariable(name, value) 
        if result is None:
            newItem = LookUpItem(name, value)
            return LookUpTable(self.items + [newItem])
        else:
            return result


    def modVariable(self, name : str, value) -> Union[None, LookUpTable]:
        """Modify a variable with the given name to the given value

        Args:
            name (str): The name of the variable to modify
            value ([type]): The value to set the variable to

        Returns:
            Union[None, LookUpTable]: Returns a new lookuptable with the modifies value if it exists, or return none if it's not found
        """
        results = list( map(lambda item: modvar(item, name, value, self.items), self.items) )
        return findFirstVar(results)


    def increaseVariable(self, name : str, value : int) -> LookUpTable:
        """Add a number to a variable

        Args:
            name (str): The name of the variable to increase 
            value (int): The value to increase the variable with 

        Returns:
            LookUpTable: The lookuptable with the increased variable
        """
        oldvalue = self.getVariable(name)
        newvalue = int(oldvalue) + int(value) 
        return self.modVariable(name, newvalue)
    
    def decreaseVariable(self, name : str, value : int) -> LookUpTable:
        """Substract a number to a variable

        Args:
            name (str): The name of the variable to decrease 
            value (int): The value to decrease the variable with 

        Returns:
            LookUpTable: The lookuptable with the decreased variable
        """
        oldvalue = self.getVariable(name)
        newvalue = int(oldvalue) - int(value) 
        return self.modVariable(name, newvalue)

    def getVariable(self, name):
        results = list( map(lambda item: item.value if item.name == name else None, self.items) )
        return findFirstVar(results)

class LookUpItem():
    def __init__(self, name : str, value):
        """Initializes a variable with 

        Args:
            name (str): The variable's name 
            value ([type]): The variable's value
        """
        self.name = name 
        self.value = value 
    

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

    def run(self, table) -> Memory:
        """Runs a memory block in memory

        Returns:
            Memory: A memory object without the previously ran memory block
        """
        if self.pc >= len(self.items):
            return None

        if type(self.items[self.pc]) == AssignmentMemoryBlock or type(self.items[self.pc]) == AssignmentModMemoryBlock:
            newpc,newtable = self.items[self.pc].run(self.pc, table) # Run the function in current memory block
        elif type(self.items[self.pc]) == WriteMemoryBlock or type(self.items[self.pc]) == IfMemoryBlock:
            newpc = self.items[self.pc].run(self.pc, table)
            newtable = table
        else:
            newpc = self.items[self.pc].run(self.pc) # Run the function in current memory block
            newtable = table
        return (Memory(self.items, newpc), newtable) # Return a new memory with(possibly) increased pc 



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

    def run(self, pc : int, table) -> int:
        """Runs the write memory block

        Args:
            pc (int): The current program counter

        Returns:
            int: The program counter after the memory block has ran
        """
        if self.isVariable:
            # Find variable in memory and grab value
            value = [table.getVariable(self.rhs[0])]

        else:
            value = self.rhs

        result = list( map(lambda word: runWrite(word, value), value) )
            
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

    def run(self, pc : int) -> int:
        """Runs the goto memory block

        Args:
            pc (int): The current program counter

        Returns:
            int:  The program counter after the memory block has ran
        """
        results = list( map(lambda item: findLabel(item, self.rhs, self.memory), self.memory.items) )
        return findFirstVar(results)
        
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

    def run(self, pc : int, table) -> int:
        """Runs the assignment memory bock

        Args:
            pc (int): The current program counter

        Returns:
            int: The program counter after the memory block ran
        """
        newtable = table.addVariable(self.lhs, self.rhs)
        return (pc + 1, newtable)

class AssignmentModMemoryBlock(MemoryBlock):
    def __init__(self, label: str, lhs: str, rhs : str, asstype : str, memory : Memory):
        """Initializes an assignment memory block

        Args:
            label (str): The memory's Label
            lhs (str): The assignment's identifier 
            rhs (str): The assignment's value
            asstype (str): The assignment's type
        """
        MemoryBlock.__init__(self, label)
        self.lhs = lhs 
        self.rhs = rhs 
        self.asstype = asstype 
        self.memory = memory

    def run(self, pc : int, table) -> Tuple[int, Memory]:
        """Runs the assignment memory bock

        Args:
            pc (int): The current program counter

        Returns:
            int: The program counter after the memory block ran
        """

        if self.asstype == "+=":
            newtable = table.increaseVariable(self.lhs, self.rhs)
        elif self.asstype == "-=":
            newtable = table.decreaseVariable(self.lhs, self.rhs)
        elif self.asstype == "=":
            newtable = table.modVariable(self.lhs, self.rhs)

        return (pc + 1, newtable)

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

    def run(self, pc : int, table) -> int:
        """Runs the if memory block

        Args:
            pc (int): The current program counter

        Returns:
            int: The program counter after the if statement
        """
        if self.compare_operator == '==':
            if str(table.getVariable(self.lhs)) == str(table.getVariable(self.rhs)):
                return pc + 1

        return pc+2

class JumpMemoryBlock(MemoryBlock):
    def __init__(self, label : str, rhs : str, isStatic : bool):
        """Initializes a Jump memory block

        Args:
            label (str): The memory block's label 
            rhs (str): The place to jump to 
            isStatic (bool): Whether the place is static or relative
        """
        self.label = label 
        self.rhs = rhs 
        self.isStatic = isStatic 
    
    def run(self, pc : int) -> int:
        """Runs the jump block

        Args:
            pc (int): The current program counter

        Returns:
            int: The program counter after the jump was run
        """
        if self.isStatic:
            return int(self.rhs)
        else:
            return pc + int(self.rhs)

class ExitMemoryBlock(MemoryBlock):
    def run(self, pc : int):
        """Runs the exit memory block

        Args:
            pc (int): The current program counter
        """
        sys.exit(0)