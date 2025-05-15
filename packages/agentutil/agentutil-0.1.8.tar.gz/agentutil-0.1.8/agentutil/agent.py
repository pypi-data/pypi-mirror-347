from abc import ABC, abstractmethod
from agentutil.utils.agentAssistant import AgentAssistant, TestAgentAssistant
from django.forms import Form


# 🎭 Abstract Base Class for Agents
class Agent(ABC):
    def __init__(self, assitant: AgentAssistant=None, form: Form=None):
        self.form = form
        if assitant:
            self.assitant = assitant
        else:
            self.assitant = TestAgentAssistant()
    @abstractmethod
    async def run(self, data):
        pass
