from typing import List, Dict
from enum import Enum

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

class Register(Enum):
    ACC = 0
    PC = 1
    IR = 2
    TEMP = 3
    IN = 4
    OUT = 5
    ADR = 6


class Interpreter:
    def __init__(self, code: List[str], input: List[int] = None, update_display=None) -> None:
        self.code: List[str] = code
        self.input: List[int] = input
        self.input_pos: int = None
        self.RAM: List[str] = [None] * 32  # Initialize RAM with 32 empty slots
        self.labels: Dict[str, int] = {}
        self.registers: Dict[Register, int] = {Register.ACC: 0, Register.PC: 0, Register.IR: 0, Register.TEMP: 0,
                                               Register.IN: None, Register.OUT: None,
                                               Register.ADR: None}  # Add this line

        self.current_line = 0
        self.load_data_into_RAM()
        self.parse()
        self.update_display = update_display
        self.registers[Register.PC] = 0
        self.terminated = False

    def load_data_into_RAM(self) -> None:
        for i, line in enumerate(self.code):
            self.RAM[i] = line.rstrip('\n')
        if self.input is not None:
            self.registers[Register.IN] = self.input[0]
            self.input_pos = 0

    def load_data(self) -> None:
        self.file = [line.rstrip('\n') for line in self.code]
        if self.input is not None:
            self.registers[Register.IN] = self.input[0]
            self.input_pos = 0

    def parse(self) -> None:
        for i in range(len(self.RAM)):
            if self.__is_label(self.RAM[i]):
                label = self.RAM[i][:-1]
                if label not in self.labels:
                    self.labels[label] = i
        # Check that all labels used in JUM and JUZ commands are defined
        for i in range(len(self.RAM)):
            line = self.RAM[i]
            if line is not None and " " in line:
                command, label = line.split(" ", 1)
                if command in ["JUM", "JUZ"] and label not in self.labels:
                    raise ValueError(f"Undefined label: {label} at line {i}")

    def run(self) -> None:
        terminated = False
        current_line = 0
        while not self.terminated:
            line: str = self.RAM[current_line]
            if line is None:
                break
            elif line.split(" ")[0].isdigit():
                # This line is data, not a command
                current_line += 1
                continue
            else:
                # Load the instruction into the IR
                self.registers[Register.IR] = line
                # Parse and execute the instruction
                command: Command = self.extract_command(line)
                self.parse_command(command, line)
                current_line += 1

            if current_line >= len(self.RAM) or self.RAM[current_line] is None:
                terminated = True

            self.registers[Register.PC] = current_line
            self.update_RAM()

            if self.update_display is not None:
                self.update_display()

    def update_RAM(self):
        for i, line in enumerate(self.RAM):
            if line is not None:
                self.RAM[i] = line.rstrip('\n')

    def step(self):
        if self.current_line < len(self.RAM):  # Change this line
            line: str = self.RAM[self.current_line]  # Change this line
            # Load the instruction into the IR
            self.registers[Register.IR] = line
            # Parse and execute the instruction
            command: Command = self.extract_command(line)
            self.parse_command(command, line)
            self.current_line += 1

            self.registers[Register.PC] = self.current_line
            self.update_RAM()

    def extract_command(self, line: str) -> Command:
        first_word = line.split(" ")[0]
        try:
            return Command[first_word]
        except KeyError:
            raise ValueError(f"Invalid command name: {first_word}")

    def parse_command(self, command: Command, line: str) -> None:
        parts = line.split(" ")
        # Load the address part of the instruction into the AR
        if len(parts) > 1:
            self.registers[Register.ADR] = int(parts[1])
        # Execute the command
        if command == Command.LOM:
            self._handle_lom(self.registers[Register.ADR])
        elif command == Command.OUT:
            self._handle_out()
        elif command == Command.STO:
            self._handle_sto(self.registers[Register.ADR])
        elif command == Command.ADD:
            self._handle_add(self.registers[Register.ADR])
        elif command == Command.SUB:
            self._handle_sub(self.registers[Register.ADR])
        elif command == Command.MUL:
            self._handle_mul(parts[1])
        elif command == Command.INR:
            self._handle_inr(parts[1])
        elif command == Command.INP:
            self._handle_inp()
        elif command == Command.AND:
            self._handle_and(parts[1])
        elif command == Command.OR:
            self._handle_or(parts[1])
        elif command == Command.XOR:
            self._handle_xor(parts[1])
        elif command == Command.NOT:
            self._handle_not(parts[1])
        elif command == Command.JUM:
            self._handle_jum(int(parts[1]))  # Change this line
        elif command == Command.JUZ:
            self._handle_juz(int(parts[1]))  # Change this line
        elif command == Command.FIN:
            self._handle_fin()

    def _handle_lom(self, address: int) -> None:
        # Load the address into the ADR register
        self.registers[Register.ADR] = address
        # Load the data from the memory address
        data = int(self.RAM[address])
        # Store the data in the ACC register
        self.registers[Register.ACC] = data
        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_out(self) -> None:
        self.registers[Register.OUT] = self.registers[Register.ACC]
        self.registers[Register.PC] += 1

    def _handle_sto(self, address: int) -> None:
        # Load the address into the ADR register
        self.registers[Register.ADR] = address
        # Store the data from the ACC register to the memory address
        self.RAM[address] = str(self.registers[Register.ACC])
        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_add(self, address: int) -> None:
        # Add the data from the memory address to the ACC register
        data = int(self.RAM[address])
        self.registers[Register.ACC] += data
        # Increment the program counter
        self.registers[Register.PC] += 1

    def _handle_sub(self, address: int) -> None:
        # Add the data from the memory address to the ACC register
        data = int(self.RAM[address])
        self.registers[Register.ACC] += data
        # Increment the program counter
        self.registers[Register.PC] -= 1

    def _handle_mul(self, val: str) -> None:
        self.registers[Register.ACC] *= int(val)
        self.registers[Register.PC] += 1


    def _handle_inr(self, reg: str) -> None:
        self.registers[Register.ACC] += 1
        self.registers[Register.PC] += 1

    def _handle_inp(self) -> None:
        self.registers[Register.ACC] = self.registers[Register.IN]
        self.registers[Register.PC] += 1

    def _handle_and(self, val: str) -> None:
        self.registers[Register.ACC] &= int(val)
        self.registers[Register.PC] += 1

    def _handle_or(self, val: str) -> None:
        self.registers[Register.ACC] |= int(val)
        self.registers[Register.PC] += 1

    def _handle_xor(self, val: str) -> None:
        self.registers[Register.ACC] ^= int(val)
        self.registers[Register.PC] += 1

    def _handle_not(self, reg: str) -> None:
        self.registers[Register.ACC] = ~self.registers[Register.ACC]
        self.registers[Register.PC] += 1

    def _handle_fin(self) -> None:
        # Set the program counter to the end of the RAM
        self.registers[Register.PC] = len(self.RAM)
        self.terminated = True

    def _handle_jum(self, address: int) -> None:
        self.registers[Register.PC] = address

    def _handle_juz(self, address: int) -> None:
        if self.registers[Register.ACC] == 0:
            self.registers[Register.PC] = address
        else:
            self.registers[Register.PC] += 1

    def __is_label(self, line: str) -> bool:
        return line is not None and line != "" and line[-1]

    def __is_comment(self, line: str) -> bool:
        return line.startswith('#')
