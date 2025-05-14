
from universal_mcp.servers.server import SingleMCPServer
from universal_mcp.integrations import AgentRIntegration
from universal_mcp.stores.store import EnvironmentStore

from universal_mcp_mailchimp.app import MailchimpApp

env_store = EnvironmentStore()
integration_instance = AgentRIntegration(name="mailchimp", store=env_store)
app_instance = MailchimpApp(integration=integration_instance)

mcp = SingleMCPServer(
    app_instance=app_instance,
)

if __name__ == "__main__":
    mcp.run()


