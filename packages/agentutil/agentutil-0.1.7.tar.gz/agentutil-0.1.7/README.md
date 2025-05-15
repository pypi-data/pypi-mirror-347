# AgentUtil

Basic classes and utilities for developing agent-based applications.

## Installation

```sh
pip install agentutil
```

Or, if you are developing locally:

```sh
pip install -e .
```

Or, if you are use `uv`:
```sh
uv add agentutil
```

## Usage

### Importing

```python
from agentutil.utils.agentAssistant import TestAgentAssistant, AgentAssistant
from agentutil.agent import Agent  # or your custom agent class
from agentutil.utils.models import News
```

### Example: Custom Assistant and Agent

```python
import asyncio
from agentutil.utils.agentAssistant import AgentAssistant
from agentutil.agent import Agent
from agentutil.utils.models import News

class SJAssistant(AgentAssistant):
    def __init__(self):
        super().__init__()

    async def publish_article(self, news: News, user_id: str):
        print("MY CUSTOM PUBLISH...")
        await asyncio.sleep(1)

    def update_news_status(
        self,
        news_id: str,
        new_status: str,
        title: str = None,
        cms_news_id: int = None,
        cost: int = None,
        duration=None
    ):
        print("MY CUSTOM UPDATE...")

assistant = SJAssistant()

# Example agent class inheriting from Agent
class MasterAgent(Agent):
    async def run(self, data):
        print("Running MasterAgent...")

agent = MasterAgent(assitant=assistant)
agent.assitant.update_news_status("master_agent", "running")

asyncio.run(agent.assitant.publish_article(News(title="Sample"), "test"))
```

## License

MIT