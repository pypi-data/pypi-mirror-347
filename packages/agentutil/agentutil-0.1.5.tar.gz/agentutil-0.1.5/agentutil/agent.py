from abc import ABC, abstractmethod
from agentutil.utils.agentAssistant import AgentAssistant, TestAgentAssistant


# 🎭 Abstract Base Class for Agents
class Agent(ABC):
    def __init__(self, assitant: AgentAssistant=None):
        if assitant:
            self.assitant = assitant
        else:
            self.assitant = TestAgentAssistant()
    @abstractmethod
    async def run(self, data):
        pass
