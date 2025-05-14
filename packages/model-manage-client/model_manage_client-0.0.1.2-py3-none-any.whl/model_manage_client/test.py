from client import ModelManageClient


def test_register():
    base_url = "https://api-am-ensaas.axa.wise-paas.com.cn/"
    client_token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhcHBOYW1lIjoiS0ItSW5zaWdodCIsImNsaWVudFR5cGUiOiJzcnAiLCJjbHVzdGVyIjoiZW5zYWFzIiwiZGF0YWNlbnRlciI6ImF4YSIsImV4cCI6NDgzNTE0NTY2OSwiaWF0IjoxNzI0NzQ1NjY5LCJpc09wZXJhdGlvbiI6ZmFsc2UsImlzcyI6Indpc2UtcGFhcyIsIm5hbWVzcGFjZSI6ImVuc2Fhcy1zZXJ2aWNlIiwicmVmcmVzaFRva2VuIjoiIiwic2NvcGVzIjpbXSwic2VydmljZU5hbWUiOiJLQi1JbnNpZ2h0IiwidG9rZW5UeXBlIjoiY2xpZW50Iiwid29ya3NwYWNlIjoiYWU5N2JmNTMtNzlkMi00YWQ3LWFlNjEtNjYzNDk5MDZkNDhiIn0.VlIYdDu7XS_2v6Tpiepmm9nUuGXmUPGPeLd8qpL6OLQhDeaVBOmP5eorfqwe_mh7hN5syG8pp3zofOpUWUsp_A"

    # Initialize CompletionClient
    m_client = ModelManageClient(base_url, client_token)

    agent_info = m_client.get_agent("test")
    if agent_info:
        print(agent_info)

    # Create Completion Message using CompletionClient
    extra_params = {
        "agent_description": "agent_description",
        "agent_icon_url": "agent_icon_url",
        "agent_api_version": "/v1.0",
        "agent_features": {},
    }
    m_client.register_agent("test", "license123", "test", **extra_params)

    # delete agent
    m_client.delete_agent("ppp")


if __name__ == "__main__":
    test_register()
