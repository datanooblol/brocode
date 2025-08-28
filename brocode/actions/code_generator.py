from . import Action, Shared
from brollm import BaseLLM
from brocode.code_analysis import MultiScriptContextBuilder
from pathlib import Path
# from broprompt import parse_codeblock_to_dict

class CodeGenerator(Action):
    def __init__(self, system_prompt:str, model:BaseLLM):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model
        self.builder = MultiScriptContextBuilder()

    def input(self):
        # 1. Ask what user wants to code
        task = input("What do you want to code? ")
        
        # 2. Ask for codebase context
        has_codebase = input("Do you have existing codebase to reference? (y/n): ").lower() == 'y'
        code_contexts = ""
        
        if has_codebase:
            codebase_path = input("Enter folder path or specific file path: ")
            # Read and process codebase
            path = Path(codebase_path)
            
            print(f"Current working directory: {Path.cwd()}")
            print(f"Trying path: {path.absolute()}")
            
            # If path doesn't exist, try relative to current working directory
            if not path.exists():
                path = Path.cwd() / codebase_path
                print(f"Trying relative path: {path.absolute()}")
            
            if not path.exists():
                print(f"Path not found: {codebase_path}")
                code_contexts = {}
            else:
                print(f"Found path: {path.absolute()}")
                if path.is_file():
                    code_contexts = self.builder.build_contexts([path])
                else:
                    # Directory - get all Python files
                    py_files = list(path.rglob("*.py"))
                    if not py_files:
                        print(f"No Python files found in: {path}")
                        code_contexts = {}
                    else:
                        code_contexts = self.builder.build_contexts(py_files)
        
        # 3. Ask for return type
        print("How do you want the output?")
        print("1. Code block in terminal")
        print("2. Save to file")
        return_type = input("Choose (1/2): ")
        
        output_path = None
        if return_type == "2":
            output_path = input("Enter file path to save: ")
        
        return {
            'task': task,
            'code_contexts': code_contexts,
            'return_type': return_type,
            'output_path': output_path
        }

    def write_py_file(self, generated_code, return_input):
        # Handle output based on return type
        if return_input['return_type'] == "2" and return_input['output_path']:
            output_path = Path(return_input['output_path'])
            # Create directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            # Write generated code to file with UTF-8 encoding
            output_path.write_text(generated_code, encoding='utf-8')
            print(f"Code saved to {output_path}")
        else:
            # Display in terminal
            print(generated_code)
            # Ask for follow-up save option
            follow_up = input("Save to file? (y/n): ")
            if follow_up.lower() == 'y':
                save_path = Path(input("Enter file path: "))
                save_path.parent.mkdir(parents=True, exist_ok=True)
                save_path.write_text(generated_code, encoding='utf-8')
                print(f"Code saved to {save_path}")        

    def parse_python_codeblock(self, response:str)->str:
        parsed = response.split("```python")[1]
        parsed = parsed.split("```")[0]
        return parsed.strip()

    def run(self, shared:Shared):
        return_input = self.input()
        # Format code contexts properly
        if return_input['code_contexts']:
            code_str = "\n\n".join([
                f"FILENAME: {filename}:\n{context}" 
                for filename, context in return_input['code_contexts'].items()
            ])
            text = f"CODEBASE (follow this codebase):\n\n{code_str}\n\nUSER:\n\n{return_input['task']}"
        else:
            text = return_input['task']
        
        messages = [self.model.UserMessage(text=text)]
        response = self.model.run(
            system_prompt=self.system_prompt,
            messages=messages
        )
        generated_code = self.parse_python_codeblock(response)
        shared.response = response
        shared.code_contexts = return_input['code_contexts']
        self.write_py_file(generated_code, return_input)
        return shared