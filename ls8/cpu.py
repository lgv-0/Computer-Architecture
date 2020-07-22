"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False

    def ram_read(self, index):
        return self.reg[index]

    def ram_write(self, val, ind):
        self.reg[ind] = val

    def load(self, fileinc):
        """Load a program into memory."""

        try:
            address = 0
            with open(fileinc) as file:
                for line in file:
                    command = line.split("#")[0].strip()
                    if command == '':
                        continue
                    self.ram[address] = int(command, 2)
                    address += 1
        
        except FileNotFoundError:
            sys.exit()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        self.running = True

        while self.running:
            command = self.ram[self.pc]
            if command == LDI:
                self.ram_write(self.ram[self.pc + 2], self.ram[self.pc + 1])
                print(f"Writing {self.ram[self.pc + 2]} to {self.ram[self.pc + 1]}")
            if command == PRN:
                value = self.ram_read(self.ram[self.pc + 1])
                print(f"{value} at {self.ram[self.pc + 1]}")
            if command == HLT:
                self.running = False
            if command == MUL:
                self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
            
            self.pc += 1 + (command >> 6)