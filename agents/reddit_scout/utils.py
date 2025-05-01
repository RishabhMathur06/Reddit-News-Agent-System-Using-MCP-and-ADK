import os

def load_instruction_from_file(filename: str, default_instruction: str = "Default instruction.") -> str:
    """Reads instruction text from a file relative to this script."""

    instruction = default_instruction

    # Construct the file path relative to this script
    # and read the instruction from the file.
    try:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, 'r', encoding="utf-8") as file:
            instruction = file.read()
        print(f"Successfully loaded instruction from {filename}.")
        
    except FileNotFoundError:
        # If the file is not found, use the default instruction.
        print(f"WARNING: Instruction file not found {filename}. Using default instruction.")

    except Exception as e:
        # Handle any other exceptions.
        print(f"ERROR: {e} loading {filename}. Using default instruction.")

    return instruction