
from universal_mcp.servers import SingleMCPServer
from universal_mcp.integrations import ApiKeyIntegration
from universal_mcp.stores import EnvironmentStore

from universal_mcp_asana.app import AsanaApp

env_store = EnvironmentStore()
integration_instance = ApiKeyIntegration(name="ASANA_API_KEY", store=env_store)
app_instance = AsanaApp(integration=integration_instance)

mcp = SingleMCPServer(
    app_instance=app_instance,
)

if __name__ == "__main__":
    mcp.run()


