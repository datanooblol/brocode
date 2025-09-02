"""Main code generator orchestrator with run function."""

from brocode.actions import Action, Shared
from brollm import BaseLLM
from brocode.code_analysis import MultiScriptContextBuilder

from ..utils import ErrorHandler, FileOperations, FileSelector, LLMHandler, UIHelper


class CodeGenerator(Action):
    """Main code generator that orchestrates all components."""
    
    def __init__(self, system_prompt: str, model: BaseLLM):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model
        
        # Initialize components
        self.error_handler = ErrorHandler()
        self.context_builder = MultiScriptContextBuilder()
        self.file_selector = FileSelector(self.context_builder, self.error_handler)
        self.file_operations = FileOperations(self.error_handler)
        self.llm_handler = LLMHandler(model, system_prompt, self.error_handler)
        self.ui_helper = UIHelper(self.file_selector)
        # Remove code_modifier from generator - handled by code_agent
    
    def handle_create_update(self, operation):
        """Handle create or update operations."""
        try:
            # For update, get target file and show preview
            target_file = None
            existing_content = ""
            
            if operation == "update":
                target_file = self.ui_helper.get_update_target_file()
                existing_content = self.ui_helper.handle_update_preview(target_file)
            
            # Get task description
            task = self.ui_helper.get_task_description(operation)
            
            # Get codebase reference
            code_contexts = self.ui_helper.get_codebase_reference()
            if code_contexts is None:  # User cancelled
                return None
            
            # Get output method
            output_choice, output_path = self.ui_helper.get_output_method()
            
            result = {
                'operation': operation,
                'task': task,
                'code_contexts': code_contexts,
                'return_type': output_choice,
                'output_path': output_path
            }
            
            # Add existing content for update operations
            if operation == "update" and target_file:
                result['target_file'] = target_file
                result['existing_content'] = existing_content
            
            return result
            
        except KeyboardInterrupt:
            return None
    
    def run(self, shared: Shared):
        """Main run function that goes straight to code generation."""
        return_input = self.handle_create_update("create")
        if return_input is not None:
            # Generate code with LLM
            result = self.llm_handler.generate_code(
                return_input['task'], 
                return_input['code_contexts']
            )
            
            if result[0] is None:  # Error occurred
                choice = result[1]
                if choice == "retry":
                    return self.run(shared)  # Retry the whole process
                else:  # skip or exit
                    return shared
            
            generated_code, response = result
            shared.response = response
            shared.code_contexts = return_input['code_contexts']
            
            # Save to file if requested
            if return_input['return_type'] == "2" and return_input['output_path']:
                self.llm_handler.save_code_to_file(generated_code, return_input['output_path'])
            
            # Offer clipboard copy
            self.llm_handler.offer_clipboard_copy(generated_code)
        
        return shared