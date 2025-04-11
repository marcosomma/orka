from .agent_base import BaseAgent

class BinaryAgent(BaseAgent):
    def run(self, input_data):
        # Placeholder logic: in real use, this would call an LLM or heuristic
        if isinstance(input_data, str) and "not" in input_data.lower():
            return False
        return True

class ClassificationAgent(BaseAgent):
    def run(self, input_data):
        # Placeholder logic: naive keyword classification
        if "why" in input_data.lower() or "how" in input_data.lower():
            return "opinion"
        elif "is" in input_data.lower() or "are" in input_data.lower():
            return "fact"
        else:
            return "question"
