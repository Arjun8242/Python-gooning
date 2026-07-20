# Name: Arjun Jaiswal

from string import Template
import re

class PromptTemplate:
    def __init__(self, name, template, description=""):
        self.name=name
        self.template=template
        self.description=description
        self.variables = {var: "" for var in re.findall(r"\{([a-zA-Z0-9_]+)\}", template)}


    def set_variable(self, key, value):
        self.variables[key] = value


    def get_variable(self, key):
        return self.variables.get(key)


    def format(self):
        results = self.template

        for key, value in self.variables.items():
            results = results.replace(f"{{{key}}}", value)

        return results
        
    def get_info(self):
        return (
            f"Name : {self.name}\n"
            f"Description : {self.description}\n"
            f"Variables : {self.variables}\n"
            f"Template : {self.template}"
        )


    def __str__(self):
        return f"{self.name} - {self.description}"


#templates store list of objects of PromptTemplate class
class PromptManager:
    def __init__(self):
        self.templates = []

    def add_template(self, template):
        if self.get_template(template.name):
            print(f"Error: Template with name '{template.name}' already exists.")
            return False
        self.templates.append(template)
        print(f"Template '{template.name}' added successfully!")
        return True


    def get_template(self, name):
        for template in self.templates:
            if template.name.lower() == name.lower():
                return template
        return None
    
    def list_templates(self):
        if len(self.templates) == 0:
            print("No templates found")
        else:
            print("\n===== All Templates =====")
            for template in self.templates:
                print(template.get_info())
                print("==========================")




    def search_templates(self, query):
        results = []

        for template in self.templates:
            if (query.lower() in template.name.lower() or
                    query.lower() in template.description.lower()):
                results.append(template)

        return results
            


    def remove_template(self, name):
        template = self.get_template(name)

        if template:
            self.templates.remove(template)
            return True

        return False
            

    
    def count(self):
        return len(self.templates)

class LLMConfig:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.7, max_tokens=1500, top_p=0.9):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p

    def update_temperature(self, temp):
        if 0.0 <= temp <= 2.0:
            self.temperature = temp
        else:
            print("Invalid temperature. Must be between 0.0 and 2.0")
    
    def update_max_tokens(self, tokens):
        if tokens > 0:
            self.max_tokens = tokens
        else:
            print("Invalid max tokens. Must be greater than 0")

    def apply_preset(self, preset_type):
        if(preset_type.lower() == "creative"):
            self.temperature = 0.9
            self.max_tokens = 2000
            self.top_p = 0.9
        elif(preset_type.lower() == "focused"):
            self.temperature = 0.2
            self.max_tokens = 500
            self.top_p = 0.5
        elif(preset_type.lower() == "balanced"):
            self.temperature = 0.7
            self.max_tokens = 1500
            self.top_p = 0.9
        else:
            print("Invalid preset type.")


    def get_config(self):
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p
        }

    def display(self):
        print("\n===== LLM Configuration =====")
        print(f"Model: {self.model}")
        print(f"Temperature: {self.temperature}")
        print(f"Max Tokens: {self.max_tokens}")
        print(f"Top P: {self.top_p}")
        print("=============================")

    

def main():
    prompt_manager = PromptManager()
    LLM_config = LLMConfig()

    while(True):
        print("\n======== PROMPT TEMPLATE SYSTEM =========")
        print("1. Create new prompt template")
        print("2. List all templates")
        print("3. Format a template")
        print("4. Search templates")
        print("5. Configure LLM settings")
        print("6. View LLM configuration")
        print("7. Exit")
        
        choice = input("\nEnter your choice: ")

        if choice == "1":
            print("\n--- Create New Prompt Template ---")
            name = input("Enter template name: ")
            template = input("Enter template string: ")
            description = input("Enter description (optional): ")

            prompt_template = PromptTemplate(name, template, description)
            prompt_manager.add_template(prompt_template)

        elif choice == "2":
            print("\n--- List All Templates ---")
            prompt_manager.list_templates()
        
        elif choice == "3":
            print("\n--- Format a Template ---")
            name = input("Enter template name: ")
            template = prompt_manager.get_template(name)

            if template:
                for var in template.variables:
                    template.set_variable(var, input(f"Enter value for {var}: "))
                print("\nFormatted Prompt:")
                print(template.format())
            else:
                print(f"Template '{name}' not found.")

        elif choice == "4":
            print("\n--- Search Templates ---")
            query = input("Enter search query: ")
            results = prompt_manager.search_templates(query)

            if results:
                print("\nSearch Results:")
                for template in results:
                    print(template.get_info())
            else:
                print("No templates found matching your query.")
        
        elif choice == "5":
            print("\n--- Configure LLM Settings ---")
            print("1. Update temperature")
            print("2. Update max tokens")
            print("3. Apply preset (creative/focused/balanced)")
            print("4. Back to main menu")

            llm_choice = input("\nEnter your choice: ")

            if llm_choice == "1":
                try:
                    temp = float(input("Enter new temperature (0.0-2.0): "))
                    LLM_config.update_temperature(temp)
                except ValueError:
                    print("Invalid input. Temperature must be a number.")
            elif llm_choice == "2":
                try:
                    tokens = int(input("Enter new max tokens (>0): "))
                    LLM_config.update_max_tokens(tokens)
                except ValueError:
                    print("Invalid input. Max tokens must be an integer.")
            elif llm_choice == "3":
                preset = input("Enter preset (creative/focused/balanced): ")
                LLM_config.apply_preset(preset)
            elif llm_choice == "4":
                pass
            else:
                print("Invalid choice.")

        elif choice == "6":
            print("\n--- View LLM Configuration ---")
            LLM_config.display()

        elif choice == "7":
            print("\nGoodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
