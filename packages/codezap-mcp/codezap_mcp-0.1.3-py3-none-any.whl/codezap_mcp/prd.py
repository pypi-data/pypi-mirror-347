import json
import requests
from .utils.callback_server import CallbackServer
import os

def get_questions_from_api(requirement: str, api_key: str) -> dict:
    """
    Get questions from the API based on user requirements.

    Args:
        requirement (str): The requirement provided by the user.
        api_key (str): The API key used for authentication.

    Returns:
        dict: A dictionary containing the API response with questions data.

    Raises:
        HTTPError: If the HTTP request to the API fails.
    """
    if os.getenv('ENV') == 'development':
        url = "http://localhost:3000/api/key_questions"
    else:
        url = "https://codezap.co/api/key_questions"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    data = {
        "user_requirement": requirement
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception if the request fails
    return response.json()

def generate_key_questions(requirement: str, api_key: str) -> str:
    """
    This tool takes a user's product requirement as input, gets questions from the CodeZap API, 
    and asks the user to select questions and options in a browser page. It then processes the 
    user's selection results and returns a formatted string containing the results.

    Args:
        requirement (str): The user's product requirement.
        api_key (str): The API key used for authentication.

    Returns:
        str: A formatted string containing the user's selection results.
    """
    try:
        # Get questions from API
        api_response = get_questions_from_api(requirement, api_key)
        
        # Process the question data returned by the API
        questions = {}
        
        # Parse the JSON string in the questions field
        questions_data = json.loads(api_response.get("questions", "{}"))
        qa_pairs = questions_data.get("qa_pairs", [])
        
        if not qa_pairs:
            raise RuntimeError("API returned incorrect data format or no question data")
            
        # Iterate through question and answer pairs
        for i, qa_pair in enumerate(qa_pairs, 1):
            question_id = f"Q{i}"
            
            # Add question and options
            questions[question_id] = {
                "question": qa_pair["question"],
                "options": qa_pair["options"] + ["Skip"]  # Add skip option
            }
        
        if not questions:
            raise RuntimeError("No valid questions and options found")
        
        # Use CallbackServer to open a browser page for user to select questions and options
        server = CallbackServer()
        result = server.prompt_user_with_options(
            title="CodeZap MCP Server: Clarify product requirements",
            questions=questions,
            timeout_seconds=300  # 5 minutes timeout
        )
        
        # Process user's selection results
        if result is None:
            # If timeout or error, return empty string
            return ""
        
        # Handle selection results for multiple questions
        selections = result.get("selections", [])
        additional_requirements = result.get("additionalRequirements", "")
        
        if not selections and not additional_requirements:
            return ""
        
        # Format selection results as a string
        formatted_results = []
        for selection in selections:
            question = selection.get("question", "")
            option = selection.get("option", "")
            is_skip = option == "Skip"  # Check if skip was selected
            
            if question and option:
                if not is_skip:
                    formatted_results.append(f"{question}: {option}")
                else:
                    # If user chose to skip, don't include this question's result
                    pass
        
        # Add user's additional requirements (if any)
        if additional_requirements and additional_requirements.strip():
            formatted_results.append(f"User's additional requirements: {additional_requirements.strip()}")

        formatted_results.append("\nNEXT_STEP: Ask the user if they want to generate tech stack, implementation plan, AI IDE rules, development tips and development process documentation. If the user agrees, summarize user's requirements and call `generate_docs`")
        
        return "\n".join(formatted_results)
    except Exception as e:
        raise RuntimeError(f"Error executing tool: {str(e)}")
