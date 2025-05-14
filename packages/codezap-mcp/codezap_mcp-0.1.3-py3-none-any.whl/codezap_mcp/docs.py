import requests
import uuid
from .utils.platform_utils import detect_platform
import os

def submit_project_details(prd: str, api_key: str) -> dict:
    """
    Submit project details to API

    Args:
        prd (str): PRD document content
        api_key (str): API key for authentication

    Returns:
        dict: API response content, including current_platform field

    Raises:
        RuntimeError: When API request fails
    """
    try:
        if os.getenv('ENV') == 'development':
            url = "http://localhost:3000/api/project-details"
        else:
            url = "https://codezap.co/api/project-details"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key
        }

        project_id = str(uuid.uuid4())
        current_platform = detect_platform()

        data = {
            "project_id": project_id,
            "prd": prd,
            "current_platform": current_platform
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        result["current_platform"] = current_platform
        result["NEXT_STEP_1"] = "Execute curl command in current folder to download all files"
        result["NEXT_STEP_2"] = "Explain the purpose of each file"
        result["NEXT_STEP_3"] = "Ask user if they want to initialize the development project, if agreed, refer to `implementation_plan.md` for project initialization"
        return result

    except Exception as e:
        raise RuntimeError(f"Failed to submit project details: {str(e)}")
