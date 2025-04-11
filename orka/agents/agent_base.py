import abc

class BaseAgent(abc.ABC):
    def __init__(self, agent_id, prompt, queue, **kwargs):
        self.agent_id = agent_id
        self.prompt = prompt
        self.queue = queue
        self.params = kwargs

    @abc.abstractmethod
    def run(self, input_data):
        '''Run the agent's reasoning process.'''
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.agent_id} queue={self.queue}>"