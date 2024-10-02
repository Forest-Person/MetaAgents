import subprocess

# Function to interact with the LLaMA model
# Function to interact with the LLaMA model with error handling for decoding issues
def llama_inference(prompt, model_path='/storage/emulated/0/Download/Replete-LLM-V2.5-Qwen-1.5b-IQ3_M.gguf'):
    command = [
        '/data/data/com.termux/files/home/llama.cpp/bin/llama-cli', '--model', model_path, '--prompt', prompt, '--ctx-size', '1028', '--n_predict', '100'
    ]
    try:
        # Use 'errors' parameter to handle decoding issues
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return f"Error with model inference: {e}"

# Define basic LLMAgent
class LLMAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def think(self, input_text):
        modified_input = f"{self.role}: {input_text}"
        response = llama_inference(modified_input)
        print(f"{self.name} Output: {response}")
        return response

# Define MetaAgent class that has access to sub-agent outputs
class MetaAgent:
    def __init__(self, name, role, sub_agents):
        self.name = name
        self.role = role
        self.sub_agents = sub_agents
        self.sub_agent_outputs = []

    def run_sub_agents(self, initial_prompt):
        # Collect outputs from sub-agents
        for agent in self.sub_agents:
            print(f"\nRunning Sub-Agent {agent.name}...")
            output = agent.think(initial_prompt)
            self.sub_agent_outputs.append(output)
        return self.sub_agent_outputs

    def think(self):
        # Meta-agent has access to all sub-agent outputs
        combined_outputs = " ".join(self.sub_agent_outputs)
        modified_input = f"{self.role}: {combined_outputs}"
        response = llama_inference(modified_input)
        print(f"\n{self.name} Meta-Agent Output: {response}")
        return response

# System for initializing agents, meta-agents, and special-purpose agents
class HierarchicalSystem:
    def __init__(self):
        self.meta_agents = []
        self.special_agents = []

    def create_special_agents(self):
        # Dynamically create agents for summarization, critical evaluation, or any other role
        num_special_agents = int(input("How many special-purpose agents would you like to create? "))
        for i in range(num_special_agents):
            name = input(f"Enter name for Special Agent {i + 1}: ")
            role = input(f"Enter role for Special Agent {name} (e.g., 'Summarize', 'Critically Evaluate'): ")
            special_agent = LLMAgent(name, role)
            self.special_agents.append(special_agent)

    def create_meta_agents(self):
        # Creating Meta-Agents
        num_meta_agents = int(input("How many meta-agents would you like to create? "))
        
        for i in range(num_meta_agents):
            meta_name = input(f"Enter name for Meta-Agent {i + 1}: ")
            meta_role = input(f"Enter role for Meta-Agent {i + 1}: ")
            
            # Creating Sub-Agents under each Meta-Agent
            sub_agents = []
            num_sub_agents = int(input(f"How many sub-agents for Meta-Agent {meta_name}? "))
            
            for j in range(num_sub_agents):
                sub_name = input(f"Enter name for Sub-Agent {j + 1} of Meta-Agent {meta_name}: ")
                sub_role = input(f"Enter role for Sub-Agent {sub_name}: ")
                sub_agents.append(LLMAgent(sub_name, sub_role))

            # Creating the Meta-Agent
            meta_agent = MetaAgent(meta_name, meta_role, sub_agents)
            self.meta_agents.append(meta_agent)

    def run_system(self, initial_prompt):
        # Process through Meta-Agents and their Sub-Agents
        all_meta_outputs = []
        for meta_agent in self.meta_agents:
            print(f"\nRunning Meta-Agent {meta_agent.name}...")
            meta_agent.run_sub_agents(initial_prompt)  # Sub-agents process the initial prompt
            meta_output = meta_agent.think()  # Meta-agent processes the combined output
            all_meta_outputs.append(meta_output)

        # Combine the outputs of all meta-agents
        combined_meta_outputs = " ".join(all_meta_outputs)

        # Process through special-purpose agents, providing them the total outputs of all meta-agents
        if self.special_agents:
            print("\nRunning Special Agents on the Combined Meta-Agent Outputs...")
            for agent in self.special_agents:
                agent.think(combined_meta_outputs)

# Main function to initialize agents and run interactions
if __name__ == "__main__":
    # Create the hierarchical system
    system = HierarchicalSystem()

    # Ask the user to dynamically create special-purpose agents (e.g., summarizers, evaluators)
    system.create_special_agents()

    # Initialize meta-agents and sub-agents
    system.create_meta_agents()

    # Get initial input from the user
    inputPrompt = input("What is the initial problem or topic to deliberate? ")

    # Run the system with the user's input
    system.run_system(inputPrompt)
