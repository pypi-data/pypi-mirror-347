
from universal_mcp.servers.server import SingleMCPServer
from universal_mcp.integrations.integration import AgentRIntegration
from universal_mcp.stores.store import EnvironmentStore

from universal_mcp_confluence.app import ConfluenceApp

env_store = EnvironmentStore()
integration_instance = AgentRIntegration(name="confluence", store=env_store)
app_instance = ConfluenceApp(integration=integration_instance)

mcp = SingleMCPServer(
    app_instance=app_instance,
)

if __name__ == "__main__":
    mcp.run()


