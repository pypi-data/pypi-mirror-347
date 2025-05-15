"""
Authentication client for FluidGrids API
"""
from typing import Dict, Optional

from .base import BaseClient
from .exceptions import FluidGridsAuthenticationError


class AuthClient(BaseClient):
    """
    Client for authentication-related operations.
    """
    
    def login(self, username: str, password: str) -> str:
        """
        Authenticate with username and password and get access token.
        
        Args:
            username: The username to authenticate with
            password: The password to authenticate with
            
        Returns:
            Access token as a string
            
        Raises:
            FluidGridsAuthenticationError: When authentication fails
        """
        try:
            # Using standard OAuth2 password flow
            data = {
                "username": username,
                "password": password,
            }
            
            response = self._request(
                method="POST",
                path="/api/v1/auth/token",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if "access_token" not in response:
                raise FluidGridsAuthenticationError("Authentication failed. No access token received.")
            
            return response["access_token"]
        except Exception as e:
            raise FluidGridsAuthenticationError(f"Authentication failed: {str(e)}")
    
    def validate_token(self) -> Dict:
        """
        Validate the current token.
        
        Returns:
            Dict containing user information if token is valid
            
        Raises:
            FluidGridsAuthenticationError: When token validation fails
        """
        # Assuming the API has an endpoint for token validation
        # This may need to be adjusted based on the actual API implementation
        try:
            return self._get("/api/v1/auth/validate")
        except Exception as e:
            raise FluidGridsAuthenticationError(f"Token validation failed: {str(e)}")
    
    def refresh_token(self, refresh_token: str) -> str:
        """
        Refresh the access token using a refresh token.
        
        Args:
            refresh_token: The refresh token
            
        Returns:
            New access token as a string
            
        Raises:
            FluidGridsAuthenticationError: When token refresh fails
        """
        # This is a placeholder for a token refresh endpoint
        # Adjust based on the actual API implementation
        try:
            data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }
            
            response = self._request(
                method="POST",
                path="/api/v1/auth/token/refresh",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if "access_token" not in response:
                raise FluidGridsAuthenticationError("Token refresh failed. No access token received.")
            
            return response["access_token"]
        except Exception as e:
            raise FluidGridsAuthenticationError(f"Token refresh failed: {str(e)}")
    
    def logout(self) -> bool:
        """
        Logout and invalidate the current token.
        
        Returns:
            True if logout was successful
            
        Raises:
            FluidGridsAuthenticationError: When logout fails
        """
        # This is a placeholder for a logout endpoint
        # Adjust based on the actual API implementation
        try:
            self._post("/api/v1/auth/logout")
            return True
        except Exception as e:
            raise FluidGridsAuthenticationError(f"Logout failed: {str(e)}") 