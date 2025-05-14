from universal_mcp.config import ServerConfig
from universal_mcp.servers.server import AgentRServer, LocalServer, SingleMCPServer


def server_from_config(config: ServerConfig):
    if config.type == "agentr":
        return AgentRServer(config=config, api_key=config.api_key)

    elif config.type == "local":
        return LocalServer(config=config)
    else:
        raise ValueError(f"Unsupported server type: {config.type}")


__all__ = [AgentRServer, LocalServer, SingleMCPServer, server_from_config]
