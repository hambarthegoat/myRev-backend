from typing import Any, Dict, Optional

def success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    return {
        "success": True,
        "message": message,
        "data": data
    }

def error_response(message: str, errors: Optional[Any] = None) -> Dict[str, Any]:
    return {
        "success": False,
        "message": message,
        "errors": errors
    }
