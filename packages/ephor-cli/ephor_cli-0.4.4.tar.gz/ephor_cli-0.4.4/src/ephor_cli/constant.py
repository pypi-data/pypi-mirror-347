import os

API_SERVER_URL = os.getenv("API_SERVER_URL", "https://mcp-hive.ti.trilogy.com/api")

AGENT_SERVER_URL = os.getenv("AGENT_SERVER_URL", "https://agents.ti.trilogy.com")

DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "mcp-hive")
