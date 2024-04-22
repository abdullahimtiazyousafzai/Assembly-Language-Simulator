import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from interpreter import Command, Register, Interpreter

class SimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulator")
        self.root.geometry("800x600")
        self.interpreter = None
        self.create_interface()
        self.cpu_entries = []
        for i, register in enumerate(Register):
            ttk.Label(self.cpu_frame, text=f"{register.name}: ").pack(side=tk.TOP)
            register_entry = ttk.Entry(self.cpu_frame)
            register_entry.pack(side=tk.TOP)
            self.cpu_entries.append(register_entry)

    def create_interface(self):
        self.create_hard_disk()
        self.create_cpu()
        self.create_ram()
        self.create_display()
        self.create_printer()
        self.create_input_register()

    def create_hard_disk(self):
        self.hard_disk_frame = ttk.LabelFrame(self.root, text="Hard Disk")
        self.hard_disk_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.load_button = ttk.Button(self.hard_disk_frame, text="Load Code File", command=self.load_code_file)
        self.load_button.pack(side=tk.TOP)

    def create_cpu(self):
        self.cpu_frame = ttk.LabelFrame(self.root, text="CPU")
        self.cpu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.run_button = ttk.Button(self.cpu_frame, text="Run", command=self.run)
        self.run_button.pack(side=tk.TOP)
        self.step_button = ttk.Button(self.cpu_frame, text="Step", command=self.step)
        self.step_button.pack(side=tk.TOP)
        self.stop_button = ttk.Button(self.cpu_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.TOP)
        self.cpu_entries = []

    def update_registers(self):
        registers = self.interpreter.registers
        for i, register in enumerate(Register):
            self.cpu_entries[i].delete(0, tk.END)
            self.cpu_entries[i].insert(0, str(registers[register]))

    def create_ram(self):
        self.ram_frame = ttk.LabelFrame(self.root, text="RAM")
        self.ram_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.ram_cells = []
        for i in range(32):
            if i == 16:
                self.ram_frame = ttk.LabelFrame(self.root, text="RAM")
                self.ram_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            cell_frame = ttk.Frame(self.ram_frame)
            cell_frame.pack(side=tk.TOP, fill=tk.X)
            cell_label = ttk.Label(cell_frame, text=f"{i}: ")
            cell_label.pack(side=tk.LEFT)
            cell_entry = ttk.Entry(cell_frame)
            cell_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.ram_cells.append(cell_entry)

    def create_display(self):
        self.display_frame = ttk.LabelFrame(self.root, text="Display")
        self.display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.display = scrolledtext.ScrolledText(self.display_frame, wrap=tk.WORD, height=5, width=40)
        self.display.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.clear_display_button = ttk.Button(self.display_frame, text="Clear Display", command=self.clear_display)
        self.clear_display_button.pack(side=tk.TOP)

    def clear_display(self):
        self.display.delete('1.0', tk.END)

    def create_printer(self):
        self.printer_frame = ttk.LabelFrame(self.root, text="Printer")
        self.printer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.printer = scrolledtext.ScrolledText(self.printer_frame, wrap=tk.WORD, height=10, width=80)
        self.printer.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def create_input_register(self):
        self.input_register_frame = ttk.LabelFrame(self.root, text="Input Register")
        self.input_register_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.input_register = ttk.Entry(self.input_register_frame)
        self.input_register.pack(side=tk.TOP)

    def load_code_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                code = file.readlines()
            print("Program loaded successfully!")

            # Load the code into the RAM cells
            for i, line in enumerate(code):
                self.ram_cells[i].delete(0, tk.END)
                self.ram_cells[i].insert(0, line)
            print("Program loaded into RAM successfully!")

            # Display the loaded code in the display widget
            for line in code:
                self.display.insert(tk.END, line)

            # Create the Interpreter instance with the code from the RAM cells
            self.interpreter = Interpreter(code, [1, 4, 7, 11, 0], self.update_display)

            # Clear the display
            self.display.delete('1.0', tk.END)

    def update_display(self):
        self.display.insert(tk.END, str(self.interpreter.registers[Register.OUT]) + '\n')

    def run(self):
        if self.interpreter is not None:
            # Read the code from the RAM cells
            code = [cell.get() for cell in self.ram_cells if cell.get() != '']
            # Create the Interpreter instance with the code from the RAM cells
            self.interpreter = Interpreter(code, [1, 4, 7, 11, 0], self.update_display)
            self.interpreter.run()
            self.update_registers()
            # Update the RAM cells with the current state of the RAM
            for i, line in enumerate(self.interpreter.RAM):
                self.ram_cells[i].delete(0, tk.END)
                if line is not None:
                    self.ram_cells[i].insert(0, line)
        print("Program executed successfully!")

    def step(self):
        if self.interpreter is not None:
            self.interpreter.step()
            self.update_registers()

    def stop(self):
        pass


root = tk.Tk()
simulator = SimulatorGUI(root)
root.mainloop()
