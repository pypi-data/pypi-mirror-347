import os
import requests

from .config import GAWX_AGENT_URL, GET_ACCESS_TOKEN_URL, GET_USER_INFO_URL, GET_SESSIONS_URL, GET_SESSION_EXECUTIONS_URL, ACCESS_TOKEN, CREATE_PIPELINE_URL, RUN_PIPELINE_URL, GET_PIPELINE_URL, CREATE_DATA_SOURCE_URL
from .config import ACCESS_TOKEN

def get_access_token(email, password):
    """
    Get an access token by email and password
    """
    response = requests.post(GET_ACCESS_TOKEN_URL, 
                             headers={"Content-Type": "application/json"},
                             json={"email": email,
                                   "password": password}
                             )
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.text}")
    else:
        return response.json()["access"]

def get_sessions():
    """
    Get all sessions
    """
    response = requests.get(GET_SESSIONS_URL, 
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    if response.status_code != 200:
        raise Exception(f"Failed to get session: {response.text}")
    else:
        sessions = response.json()
        return sessions
    
def get_session(session_id):
    """
    Get a session by id
    """
    session_url = f"{GET_SESSIONS_URL}{session_id}/"
    print(session_url)
    response = requests.get(session_url, 
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    if response.status_code != 200:
        print("Failed to get session:", response.text, response.status_code)
        raise Exception(f"Failed to get session: {response.text}")
    else:
        session = response.json()
        return session

def get_session_executions(session_id):
    """
    Get session executions by session id
    """
    session_execution_url = f"{GET_SESSION_EXECUTIONS_URL}{session_id}"
    response = requests.get(session_execution_url, 
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    if response.status_code != 200:
        raise Exception(f"Failed to get session execution: {response.text}")
    else:
        return response.json()
    
def create_data_source(name, description, type, files):
    """
    Create a data source
    """
    response = requests.post(CREATE_DATA_SOURCE_URL, 
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
                            files=files,
                            data={"name": name,
                                  "description": description,
                                  "type": type})
    if response.status_code == 201:
        print("Data source created successfully")
        return {"data": response.json(), "status": "success"}
    else:
        print("Failed to create data source")
        return {"data": None, "status": "error", "message": response.text}
    
def create_pipeline(session_id, vector_db_id, data_sources):
    """
    Create a pipeline
    """
    response = requests.post(CREATE_PIPELINE_URL, 
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
                            json={"session_id": session_id,
                                  "vector_db": vector_db_id,
                                  "data_sources": data_sources,
                                  "action": "create"})
    print("status code:", response.status_code)
    if response.status_code == 201:
        print("Pipeline created successfully")
        return {"data": response.json(), "status": "success"}
    else:
        print("Failed to create pipeline")
        return {"data": None, "status": "error", "message": response.text}
    
def run_pipeline(pipeline_id):
    """
    Run a pipeline by id
    """
    print("Running pipeline...")
    response = requests.post(RUN_PIPELINE_URL, 
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
                            json={"pipeline_id": pipeline_id,
                                  "action": "run"})
    if response.status_code == 200:
        print("Pipeline run successfully")
        return {"data": response.json(), "status": "success"}
    else:
        print("Failed to run pipeline:", response.text)
        return {"data": None, "status": "error", "message": response.text}
    
def get_pipeline(pipeline_id):
    """
    Get a pipeline by id
    """
    print("Getting pipeline...")
    response = requests.get(f"{GET_PIPELINE_URL}{pipeline_id}/", 
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    if response.status_code == 200:
        print("Pipeline retrieved successfully")
        return {"data": response.json(), "status": "success"}
    else:
        print("Failed to retrieve pipeline:", response.text)
        return {"data": None, "status": "error", "message": response.text}
