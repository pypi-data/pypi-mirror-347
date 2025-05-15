"""
Base client for all FluidGrids API clients
"""
import json
from typing import Any, Dict, Optional, Union
import requests
from requests.exceptions import RequestException

from .exceptions import (
    FluidGridsAPIError,
    FluidGridsAuthenticationError,
    FluidGridsError,
    FluidGridsResourceNotFoundError,
    FluidGridsValidationError,
)


class BaseClient:
    """
    Base client for FluidGrids API.
    
    All API-specific clients inherit from this class.
    """
    
    def __init__(self, client):
        """Initialize with parent FluidGridsClient instance"""
        self._client = client
        
    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to the FluidGrids API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API path (will be appended to base_url)
            params: Query parameters
            data: Form data
            json_data: JSON body data
            headers: Additional headers
            
        Returns:
            Response data as a dictionary
            
        Raises:
            FluidGridsAuthenticationError: When authentication fails
            FluidGridsResourceNotFoundError: When the requested resource is not found
            FluidGridsValidationError: When the request data is invalid
            FluidGridsAPIError: For other API errors
            FluidGridsError: For unexpected errors
        """
        url = f"{self._client.base_url}{path}"
        
        # Merge auth headers with any additional headers
        request_headers = self._client.auth_headers.copy()
        if headers:
            request_headers.update(headers)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=request_headers,
            )
            
            # Raise appropriate exceptions based on status code
            if response.status_code == 401:
                raise FluidGridsAuthenticationError("Authentication failed. Check your credentials.")
            if response.status_code == 403:
                raise FluidGridsAuthenticationError("You don't have permission to access this resource.")
            if response.status_code == 404:
                raise FluidGridsResourceNotFoundError(f"Resource not found: {path}")
            if response.status_code == 422:
                raise FluidGridsValidationError(f"Validation error: {response.text}")
            if response.status_code >= 400:
                raise FluidGridsAPIError(f"API error ({response.status_code}): {response.text}")
            
            # Return response data
            if response.text:
                return response.json()
            return {}
            
        except RequestException as e:
            raise FluidGridsError(f"Error connecting to FluidGrids API: {str(e)}")
        except json.JSONDecodeError:
            raise FluidGridsError(f"Invalid JSON response from API: {response.text if 'response' in locals() else 'No response'}")
    
    def _get(self, path: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Shortcut for GET requests"""
        return self._request("GET", path, params=params, **kwargs)
    
    def _post(self, path: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Shortcut for POST requests"""
        return self._request("POST", path, json_data=json_data, **kwargs)
    
    def _put(self, path: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Shortcut for PUT requests"""
        return self._request("PUT", path, json_data=json_data, **kwargs)
    
    def _delete(self, path: str, **kwargs) -> Dict[str, Any]:
        """Shortcut for DELETE requests"""
        return self._request("DELETE", path, **kwargs) 