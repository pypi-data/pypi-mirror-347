import os

GAWX_SERVER_URL = os.getenv("GAWX_SERVER_URL")
ACCESS_TOKEN = os.getenv("GAWX_ACCESS_TOKEN")
GAWX_AGENT_URL = os.getenv("GAWX_AGENT_URL")

GET_ACCESS_TOKEN_URL = f"{GAWX_SERVER_URL}/api/token/"
GET_USER_INFO_URL = f"{GAWX_SERVER_URL}/api/user/"
GET_SESSIONS_URL = f"{GAWX_SERVER_URL}/api/v1/session/"
GET_SESSION_EXECUTIONS_URL = f"{GAWX_SERVER_URL}/api/v1/session_operation/?session="

CREATE_PIPELINE_URL = f"{GAWX_SERVER_URL}/api/v1/pipelines/"
RUN_PIPELINE_URL = f"{GAWX_SERVER_URL}/api/v1/pipelines/"
GET_PIPELINE_URL = f"{GAWX_SERVER_URL}/api/v1/pipelines/"

CREATE_DATA_SOURCE_URL = f"{GAWX_SERVER_URL}/api/v1/data_source/create/"