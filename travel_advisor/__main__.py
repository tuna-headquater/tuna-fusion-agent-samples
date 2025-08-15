from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from executor import TravelPlannerAgentExecutor


if __name__ == '__main__':
    skill = AgentSkill(
        id='travel_planner',
        name='travel planner agent',
        description='travel planner',
        tags=['travel planner'],
        examples=['hello', 'nice to meet you!'],
    )

    agent_card = AgentCard(
        name='travel planner Agent',
        description='travel planner',
        url='http://localhost:8082/a2a/namespaces/a2a-samples-ns/agents/travel-advisor-deploy',
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=TravelPlannerAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AFastAPIApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    import uvicorn

    uvicorn.run(server.build(
        agent_card_url='/a2a/namespaces/a2a-samples-ns/agents/travel-advisor-deploy/.well-known/agent.json',
        rpc_url='/a2a/namespaces/a2a-samples-ns/agents/travel-advisor-deploy',
    ), port=8082)