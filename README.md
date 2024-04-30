# Assembly Language Simulator

This project is a simple assembly code simulator built with Python and Tkinter. It allows you to load assembly code from a file, run it, and see the results in a GUI.

## Features

- Load assembly code from a file
- Run the loaded code
- Step through the code one line at a time
- View the state of the CPU registers and RAM
- View the output of the code

## Instruction Set

The simulator supports the following instructions:

- LOM: Load the data from the memory address into the ACC register. Format: `LOM <address>`
- OUT: Output the value in the ACC register. Format: `OUT`
- STO: Store the data from the ACC register to the memory address. Format: `STO <address>`
- ADD: Add the data from the memory address to the ACC register. Format: `ADD <address>`
- SUB: Subtract the data from the ACC register. Format: `SUB <address>`
- MUL: Multiply the ACC register by the data from the memory address. Format: `MUL <address>`
- INR: Increment the register specified by the AR register. Format: `INR`
- INP: Load the value from the INPR register into the ACC register. Format: `INP`
- AND: Perform a bitwise AND operation on the ACC register and the data from the memory address. Format: `AND <address>`
- OR: Perform a bitwise OR operation on the ACC register and the data from the memory address. Format: `OR <address>`
- XOR: Perform a bitwise XOR operation on the ACC register and the data from the memory address. Format: `XOR <address>`
- NOT: Perform a bitwise NOT operation on the ACC register. Format: `NOT`
- JUM: Jump to the memory address specified by the AR register. Format: `JUM <address>`
- JUZ: Jump to the memory address specified by the AR register if the ACC register is zero. Format: `JUZ <address>`
- FIN: Finish the program execution. Format: `FIN`

In the above formats, `<address>` represents the memory address to be used by the instruction.

## Registers

The simulator uses the following registers:

- ACC: Accumulator register
- PC: Program counter
- IR: Instruction register
- DR: Data register
- CTR: Counter register
- OUTR: Output register
- AR: Address register
- INPR: Input register

## Usage

1. Clone the repository to your local machine.
2. Run `simulator.exe` from `dist/`to start the simulator or run the `simulator.py` file in any python supported IDE (ensure both the `simulator.py` and `interpreter.py` are in the same project).
3. Click the "Load Code File" button to load assembly code from a file.
4. Click the "Run" button to run the loaded code.
5. Click the "Step" button to step through the code one line at a time.

## Dependencies

- Python 3.10
- Tkinter

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
