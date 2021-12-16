import re
import argparse

MAPPINGS = {
    '+': 'add',
    '-': 'subtract',
    '>': 'increment_pointer',
    '<': 'decrement_pointer',
    '.': 'output',
    ',': 'input',
    '[': 'skip_open',
    ']': 'skip_close'
}


class Brainfuck:
    def __init__(self, file_name, show_array=False, stackSize=0):
        self.stackSize = stackSize
        if(stackSize > 128000):
            print("Stack size must be below 128,000.")
            exit()
        elif(stackSize < 2048):
            print("Stack size cannot be equal to 2048 or under.")
            exit()
        print("Initializing Stack...")
        print("-------------- PROGRAM OUTPUT --------------\n")
        self.data = [0 for i in range(stackSize)]
        self.data_pointer = 0
        self.instruction_pointer = 0
        self.program = ''
        self.show_array = show_array

        with open(file_name, 'r') as f:
            program = f.read()
            self.program = re.sub('[^\+\-<>.,\[\]]', '', program)

        self.parens = self.find_pairs(self.program)
        self.invparens = {v: k for k, v in self.parens.items()}

    def run(self):
        while self.instruction_pointer < len(self.program):
            func = getattr(self,
                           MAPPINGS.get(self.program[self.instruction_pointer]))
            if func:
                func()
            self.instruction_pointer += 1
        print("\n-------------- PROGRAM END --------------")
        if self.show_array:
            print("Array:", self.data[:self.program.count('>')])

    def find_pairs(self, program):
        pairs = {}
        stack = []

        for i, c in enumerate(program):
            if c == '[':
                stack.append(i)
            elif c == ']':
                if len(stack) == 0:
                    raise IndexError("No matching closing bracket for %i" % i)
                pairs[stack.pop()] = i

        if len(stack) > 0:
            raise IndexError("No matching opening bracket for %i" % i)

        return pairs

    def add(self):
        self.data[self.data_pointer] += 1

    def subtract(self):
        self.data[self.data_pointer] -= 1

    def increment_pointer(self):
        if self.data_pointer < self.stackSize:
            self.data_pointer += 1

    def decrement_pointer(self):
        if self.data_pointer > 0:
            self.data_pointer -= 1

    def output(self):
        print(chr(self.data[self.data_pointer]), end='')

    def input(self):
        valid = False

        while True:
            try:
                data = int(input("Stdin: "))
                if 0 <= data <= 127:
                    break
                print("Input must be an integer less than 127.\n")
            except ValueError:
                print("Please input numbers only.\n")
                exit()

        self.data[self.data_pointer] = data

    def skip_open(self):
        if self.data[self.data_pointer] == 0:
            self.instruction_pointer = self.parens[self.instruction_pointer]

    def skip_close(self):
        if self.data[self.data_pointer] != 0:
            self.instruction_pointer = self.invparens[self.instruction_pointer]


parser = argparse.ArgumentParser('Execute a brainfuck program.')
parser.add_argument('file_name', metavar='file', type=str,
                    help='Name of brainfuck program.')
parser.add_argument('-d', dest='show_array', action='store_true',
                    help='Show data array at the end of execution.')
parser.add_argument('stackSize', metavar='stack_size', type=int, help='Set a custom stack size')

if __name__ == "__main__":
    args = parser.parse_args()

    bf = Brainfuck(args.file_name, show_array=args.show_array, stackSize=args.stackSize)
    bf.run()