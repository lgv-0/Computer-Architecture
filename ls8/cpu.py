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
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b10000010
            else:
                self.flag = 0b00000100
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

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        ADD = 0b10100000
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        self.running = True

        while self.running:
            command = self.ram[self.pc]
            if command == LDI:
                self.ram_write(self.ram[self.pc + 2], self.ram[self.pc + 1])
            elif command == PRN:
                value = self.ram_read(self.ram[self.pc + 1])
                print(f"{value} at {self.ram[self.pc + 1]}")
            elif command == HLT:
                self.running = False
            elif command == MUL:
                self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
            elif command == PUSH:
                self.reg[7] -= 1
                sp = self.reg[7]
                reg_index = self.ram[self.pc + 1]
                self.ram[sp] = self.reg[reg_index]
            elif command == POP:
                sp = self.reg[7]
                popped_value = self.ram[sp]
                reg_index = self.ram[self.pc + 1]
                self.reg[reg_index] = popped_value
                self.reg[7] += 1
            elif command == CALL:
                reg_idx = self.ram[self.pc + 1]
                jump_address = self.reg[reg_idx]
                return_address = self.pc + 2
                self.reg[7] -= 1
                sp = self.reg[7]
                self.ram[sp] = return_address
                self.pc = jump_address
                continue
            elif command == RET:
                sp = self.reg[7]
                return_address = self.ram[sp]
                self.reg[7] += 1
                self.pc = return_address
                continue
            elif command == CMP:
                self.alu("CMP", self.ram[self.pc + 1], self.ram[self.pc + 2])
            elif command == JMP:
                jump_address = self.reg[self.ram[self.pc + 1]]
                self.pc = jump_address
                continue
            elif command == JEQ:
                if self.flag is None:
                    # W h a t ?
                    print("What messed up ? ? ?")
                elif self.flag == 0b00000001:
                    jump_address = self.reg[self.ram[self.pc + 1]]
                    self.pc = jump_address
                    continue
            elif command == JNE:
                if self.flag is None:
                    # W h a t ?
                    print("What messed up ? ? ?")
                elif self.flag != 0b00000001:
                    jump_address = self.reg[self.ram[self.pc + 1]]
                    self.pc = jump_address
                    continue
            
            self.pc += 1 + (command >> 6)