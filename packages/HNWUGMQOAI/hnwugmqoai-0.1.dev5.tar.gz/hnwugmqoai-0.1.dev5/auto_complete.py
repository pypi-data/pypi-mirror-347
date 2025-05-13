from core.scheduler.agentManager import AgentModel


def complete_model(ctx, param, incomplete):
    return [name for name in AgentModel.__members__.values()]