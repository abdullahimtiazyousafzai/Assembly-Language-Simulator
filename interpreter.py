from typing import List, Dict
from enum import Enum
from tkinter import messagebox

class Command(Enum):
    LOM = 0
    OUT = 1 # changed to out
    STO = 2
    ADD = 3
    SUB = 4
    MUL = 5
    JUM = 6
    JUZ = 7
    INR = 8
    INP = 9 # changed to INR
    AND = 10
    OR = 11
    XOR = 12
    NOT = 13
    FIN = 14
    DEC = 15  # decrement


class Register(Enum):
    ACC = 0
    PC = 1
    IR = 2
    DR = 3
    CTR = 4  # counter
    OUTR = 5
    AR = 6
    INPR = 7  # input register



def extract_command(line: str) -> Command:
    first_word = line.split(" ")[0]
    if not first_word:
        # If the first word is an empty string, return None or raise an error
        return None
    try:
        return Command[first_word]
    except KeyError:
        raise ValueError(f"Invalid command name: {first_word}")


class Interpreter:
    def __init__(self, code: List[str], update_display=None) -> None:
        self.code: List[str] = code
        self.input_pos: int = None
        self.RAM: List[str] = [None] * 32  # Initialize RAM with 32 empty slots
        self.registers: Dict[Register, int] = {Register.ACC: 0, Register.PC: 0, Register.IR: 0, Register.DR: 0,
                                               Register.INPR: None, Register.OUTR: None,
                                               Register.AR: None, Register.CTR: 0}  # Add this line

        self.load_data_into_RAM()
        self.update_display = update_display
        self.finished = False

    def load_data_into_RAM(self) -> None:
        for i, line in enumerate(self.code):
            self.RAM[i] = line.rstrip('\n')

    def load_data(self) -> None:
        self.file = [line.rstrip('\n') for line in self.code]

    def run(self) -> None:
        while not self.finished:
            self.step()

    def update_RAM(self):
        for i, line in enumerate(self.RAM):
            if line is not None:
                self.RAM[i] = line.rstrip('\n')

    def step(self):
        if self.registers[Register.PC] < len(self.RAM) and not self.finished:
            line: str = self.RAM[self.registers[Register.PC]]
            # Load the instruction into the IR
            self.registers[Register.IR] = line
            # Pse and execute the instruction
            command: Command = extract_command(line)
            self.pse_command(command, line)

            def stop(self):
                if self.interpreter is not None:
                    self.interpreter.finished = True
                    print("Program execution stopped!")

            if self.update_display is not None and self.registers[Register.OUTR] is not None:
                self.update_display()

            self.update_RAM()
        else:
            messagebox.showinfo("Program Finished", "The program has finished executing.")

    def pse_command(self, command: Command, line: str) -> None:
        pts = line.split(" ")
        # Load the address pt of the instruction into the
        if len(pts) > 1:
            self.registers[Register.AR] = int(pts[1])
        # Execute the command
        if command == Command.LOM:
            self._handle_lom()
        elif command == Command.OUT:
            self._handle_out()
        elif command == Command.STO:
            self._handle_sto()
        elif command == Command.ADD:
            self._handle_add()
        elif command == Command.SUB:
            self._handle_sub()
        elif command == Command.MUL:
            self._handle_mul()
        elif command == Command.INR:
            self._handle_inr()
        elif command == Command.INP:
            self._handle_inp()
        elif command == Command.AND:
            self._handle_and()
        elif command == Command.OR:
            self._handle_or()
        elif command == Command.XOR:
            self._handle_xor()
        elif command == Command.NOT:
            self._handle_not()
        elif command == Command.JUM:
            self._handle_jum()
        elif command == Command.JUZ:
            self._handle_juz()
        elif command == Command.FIN:
            self._handle_fin()

    def _handle_lom(self) -> None:
        # Load the data from the memory address
        data = int(self.RAM[self.registers[Register.AR]])
        # Store the data in the ACC register
        self.registers[Register.DR] = data
        self.registers[Register.ACC] = self.registers[Register.DR]
        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_out(self) -> None:
        self.registers[Register.OUTR] = self.registers[Register.ACC]
        self.registers[Register.PC] += 1

    def _handle_sto(self) -> None:
        # Store the data from the ACC register to the memory address
        self.RAM[self.registers[Register.AR]] = str(self.registers[Register.ACC])
        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_add(self) -> None:
        # Add the data from the memory address to the ACC register
        data = int(self.RAM[self.registers[Register.AR]])
        self.registers[Register.ACC] += data
        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_sub(self) -> None:
        # Subtract the data from the memory address from the ACC register
        data = int(self.RAM[self.registers[Register.AR]])
        self.registers[Register.ACC] -= data
        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_mul(self) -> None:
        # Multiply the ACC register by the data from the memory address
        data = int(self.RAM[self.registers[Register.AR]])
        self.registers[Register.CTR] = -data

        # Initialize DR with the current value of ACC
        self.registers[Register.CTR] += 1
        while self.registers[Register.CTR] != 0:
            # Add DR to ACC (repeated addition)
            self.registers[Register.ACC] += self.registers[Register.DR]
            # Increment the CTR to simulate multiplication by repeated addition
            self.registers[Register.CTR] += 1

        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_inr(self) -> None:
        # Increment the register specified by the AR register
        self.registers[Register.ACC] += 1
        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_inp(self) -> None:
        self.registers[Register.ACC] = self.registers[Register.INPR]
        self.registers[Register.PC] += 1

    def _handle_and(self) -> None:
        # Perform a bitwise AND operation on the ACC register and the data from the memory address
        data = int(self.RAM[self.registers[Register.AR]])
        self.registers[Register.ACC] &= data
        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_or(self) -> None:
        # Perform a bitwise OR operation on the ACC register and the data from the memory address
        data = int(self.RAM[self.registers[Register.AR]])
        self.registers[Register.ACC] |= data
        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_xor(self) -> None:
        # Perform a bitwise XOR operation on the ACC register and the data from the memory address
        data = int(self.RAM[self.registers[Register.AR]])
        self.registers[Register.ACC] ^= data
        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_not(self) -> None:
        # Perform a bitwise NOT operation on the ACC register
        self.registers[Register.ACC] = ~self.registers[Register.ACC]
        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_fin(self) -> None:
        self.finished = True

    def _handle_jum(self) -> None:
        adr = self.registers[Register.AR]
        if 0 <= adr < len(self.RAM):
            self.registers[Register.PC] = adr
            self.jump_occurred = True  # Set the flag
        else:
            raise ValueError("Invalid memory address for JUM instruction")

    def _handle_juz(self) -> None:
        if self.registers[Register.ACC] == 0:
            adr = self.registers[Register.AR]
            if 0 <= adr < len(self.RAM):
                self.registers[Register.PC] = adr
                self.jump_occurred = True  # Set the flag
            else:
                raise ValueError("Invalid memory address for JUZ instruction")
        else:
            self.registers[Register.PC] += 1

    def __is_comment(self, line: str) -> bool:
        return line.sttswith('#')
