#!/usr/bin/env python3
"""
Three-Address Code Generator
Generates intermediate code from CSV files containing arithmetic expressions.
Enhanced with proper structure, error handling, and documentation.
"""

import pandas as pd
import sys
import os
from datetime import datetime
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class GeneratorConfig:
    """Configuration for code generator"""
    output_dir: str = "OUTPUT_INTERMEDIATE_CODE_GENERATOR"
    supported_operators: str = "+-*/"
    register_prefix: str = "R"


class OutputManager:
    """Manages dual output to console and file"""
    
    def __init__(self, output_dir: str, timestamp: str = None):
        self.output_dir = output_dir
        self.timestamp = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.setup_output()
    
    def setup_output(self):
        """Create output directory and file"""
        os.makedirs(self.output_dir, exist_ok=True)
        self.output_file = open(
            os.path.join(self.output_dir, f"output_{self.timestamp}.txt"),
            'w'
        )
        self.original_stdout = sys.stdout
        sys.stdout = self
    
    def write(self, data: str):
        """Write to both console and file"""
        self.original_stdout.write(data)
        self.output_file.write(data)
        self.flush()
    
    def flush(self):
        """Flush both outputs"""
        self.original_stdout.flush()
        self.output_file.flush()
    
    def close(self):
        """Close file and restore stdout"""
        sys.stdout = self.original_stdout
        self.output_file.close()
        output_path = os.path.join(self.output_dir, f"output_{self.timestamp}.txt")
        print(f"\n[SUCCESS] Output saved to: {output_path}")


class ThreeAddressCodeGenerator:
    """Generates three-address code from CSV expressions"""
    
    def __init__(self, config: GeneratorConfig = None):
        self.config = config or GeneratorConfig()
        self.dataframe = None
        self.variables = []
        self.operators = []
        self.registers = []
        self.register_map = {}
    
    def load_csv(self, filename: str) -> bool:
        """Load and validate CSV file"""
        try:
            self.dataframe = pd.read_csv(filename)
            
            # Validate columns
            if list(self.dataframe.columns) != ['left', 'right']:
                print("ERROR: CSV must have exactly 'left' and 'right' columns")
                return False
            
            print(f"\nInput CSV file: {filename}")
            print(f"Expressions to process: {len(self.dataframe)}\n")
            print(self.dataframe)
            return True
        
        except FileNotFoundError:
            print(f"ERROR: File '{filename}' not found.")
            return False
        except Exception as e:
            print(f"ERROR loading CSV: {e}")
            return False
    
    def extract_elements(self):
        """Extract variables, operators, and allocate registers"""
        elements = []
        
        # Collect all elements from left and right sides
        for _, row in self.dataframe.iterrows():
            elements.append(row['left'])
            elements.extend(row['right'].split())
        
        # Separate operators and variables
        operators_found = set()
        for elem in elements:
            if elem in self.config.supported_operators:
                operators_found.add(elem)
        
        self.operators = list(operators_found)
        
        # Get unique variables (exclude operators)
        variables = set(elem for elem in elements if elem not in self.operators)
        self.variables = sorted(list(variables))
        
        # Allocate registers to variables
        self.registers = [f"{self.config.register_prefix}{i}" for i in range(len(self.variables))]
        self.register_map = dict(zip(self.variables, self.registers))
        
        return True
    
    def get_register(self, variable: str) -> str:
        """Get register for a variable"""
        return self.register_map.get(variable, None)
    
    def generate_code(self):
        """Generate three-address code for all expressions"""
        print("\n" + "="*60)
        print("GENERATED THREE-ADDRESS CODE")
        print("="*60 + "\n")
        
        try:
            for idx, (_, row) in enumerate(self.dataframe.iterrows()):
                left_var = row['left']
                right_expr = row['right'].split()
                
                print(f"# Expression {idx + 1}: {left_var} = {row['right']}")
                self._generate_for_expression(left_var, right_expr)
                print()
        
        except Exception as e:
            print(f"ERROR generating code: {e}")
            return False
        
        return True
    
    def _generate_for_expression(self, target: str, expression: List[str]):
        """Generate code for a single expression"""
        target_reg = self.get_register(target)
        
        # Simple case: single value (variable or number)
        if len(expression) == 1:
            value = expression[0]
            value_reg = self.get_register(value) if not value.isdigit() else f"#{value}"
            print(f"  MOV {value} , {target_reg}")
            return
        
        # Complex case: operations
        registers_used = []
        i = 0
        
        while i < len(expression):
            if i == 0:
                # First operand
                operand = expression[i]
                operand_reg = self.get_register(operand) if not operand.isdigit() else f"#{operand}"
                print(f"  MOV {operand} , {operand_reg}")
                registers_used.append(operand_reg)
                i += 1
            
            elif i < len(expression) - 1 and expression[i] in self.config.supported_operators:
                # Operator and next operand
                operator = expression[i]
                next_operand = expression[i + 1]
                next_operand_reg = self.get_register(next_operand) if not next_operand.isdigit() else f"#{next_operand}"
                
                print(f"  MOV {next_operand} , {next_operand_reg}")
                registers_used.append(next_operand_reg)
                
                # Perform operation
                op_code = self._get_operation_code(operator)
                if registers_used:
                    print(f"  {op_code} {registers_used[-2]} , {registers_used[-1]}")
                
                i += 2
            
            else:
                i += 1
        
        # Store result in target
        if registers_used:
            print(f"  STOR {registers_used[-1]} , {target_reg}")
    
    def _get_operation_code(self, operator: str) -> str:
        """Map operator to instruction code"""
        ops = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV'
        }
        return ops.get(operator, 'UNKNOWN')
    
    def print_statistics(self):
        """Print generation statistics"""
        print("="*60)
        print("GENERATION STATISTICS")
        print("="*60)
        print(f"Total expressions processed: {len(self.dataframe)}")
        print(f"Unique variables: {len(self.variables)}")
        print(f"Registers allocated: {len(self.registers)}")
        print(f"Operators used: {', '.join(self.operators)}")
        print(f"\nRegister Mapping:")
        for var, reg in self.register_map.items():
            print(f"  {var} -> {reg}")


def main():
    """Main entry point"""
    # Print header
    print("="*60)
    print("THREE-ADDRESS CODE GENERATOR")
    print("="*60)
    print("Generating intermediate code from CSV expressions\n")
    
    # Setup output management
    output_mgr = OutputManager(GeneratorConfig.output_dir)
    
    try:
        # Get input file
        csv_file = sys.argv[1] if len(sys.argv) > 1 else "input.csv"
        
        if sys.argv[1:]:
            print(f"Using custom input file: {csv_file}\n")
        
        # Create and run generator
        config = GeneratorConfig()
        generator = ThreeAddressCodeGenerator(config)
        
        # Load CSV
        if not generator.load_csv(csv_file):
            return 1
        
        # Extract elements and allocate registers
        if not generator.extract_elements():
            return 1
        
        # Generate code
        if not generator.generate_code():
            return 1
        
        # Print statistics
        generator.print_statistics()
        
        return 0
    
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        return 1
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        output_mgr.close()


if __name__ == "__main__":
    sys.exit(main())
