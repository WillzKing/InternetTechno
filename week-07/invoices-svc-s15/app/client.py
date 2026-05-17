import requests
from typing import Dict, Any, Optional

PROJECT_CODE = "logs-s15"

GRAPHQL_URL = "http://localhost:8139/graphql"

def build_payload(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    return payload

def send_query(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload = build_payload(query, variables)
    response = requests.post(GRAPHQL_URL, json=payload)
    result = response.json()
    
    if "errors" in result:
        print("Ошибки:")
        for error in result["errors"]:
            print(f"  - {error['message']}")
    
    if "data" in result:
        print("Данные:")
        print(result["data"])
    
    return result

if __name__ == "__main__":
    mutation = """
    mutation($name: String!, $level: String!) {
        createLog(name: $name, level: $level) {
            id
            name
            level
            createdAt
        }
    }
    """
    variables = {"name": "Тестовый лог", "level": "INFO"}
    
    print("=== Создание лога (mutation) ===")
    send_query(mutation, variables)
    
    query = """
    {
        logs {
            id
            name
            level
            createdAt
        }
    }
    """
    
    print("\n=== Получение логов (query) ===")
    send_query(query)
    
    single_query = """
    query($id: Int!) {
        log(id: $id) {
            id
            name
            level
            createdAt
        }
    }
    """
    
    print("\n=== Получение лога по ID ===")
    send_query(single_query, {"id": 1})