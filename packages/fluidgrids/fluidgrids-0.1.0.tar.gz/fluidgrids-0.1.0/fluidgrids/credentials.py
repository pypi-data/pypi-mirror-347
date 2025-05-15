"""
Credentials client for FluidGrids API
"""
from typing import Any, Dict, List, Optional

from .base import BaseClient
from .models import CredentialCreate, CredentialDetail, CredentialSummary, CredentialUpdate


class CredentialClient(BaseClient):
    """
    Client for credential-related operations.
    """
    
    def list(self) -> List[CredentialSummary]:
        """
        List all credentials.
        
        Returns:
            List of credential summaries
        """
        response = self._get("/api/v1/credentials")
        return [CredentialSummary.model_validate(cred) for cred in response]
    
    def get(self, credential_id: str) -> CredentialDetail:
        """
        Get a specific credential.
        
        Args:
            credential_id: The credential ID
            
        Returns:
            Credential detail
        """
        response = self._get(f"/api/v1/credentials/{credential_id}")
        return CredentialDetail.model_validate(response)
    
    def create(self, credential: CredentialCreate) -> CredentialDetail:
        """
        Create a new credential.
        
        Args:
            credential: The credential to create
            
        Returns:
            Created credential detail
        """
        response = self._post(
            "/api/v1/credentials",
            json_data=credential.model_dump(exclude_unset=True),
        )
        return CredentialDetail.model_validate(response)
    
    def update(self, credential_id: str, credential: CredentialUpdate) -> CredentialDetail:
        """
        Update a credential.
        
        Args:
            credential_id: The credential ID
            credential: The credential update data
            
        Returns:
            Updated credential detail
        """
        response = self._put(
            f"/api/v1/credentials/{credential_id}",
            json_data=credential.model_dump(exclude_unset=True),
        )
        return CredentialDetail.model_validate(response)
    
    def delete(self, credential_id: str) -> None:
        """
        Delete a credential.
        
        Args:
            credential_id: The credential ID
        """
        self._delete(f"/api/v1/credentials/{credential_id}")
    
    def get_types(self) -> List[Dict[str, Any]]:
        """
        Get available credential types.
        
        Returns:
            List of credential type information
        """
        return self._get("/api/v1/credentials/types")
    
    def get_type_schema(self, credential_type: str) -> Dict[str, Any]:
        """
        Get schema for a specific credential type.
        
        Args:
            credential_type: The credential type
            
        Returns:
            Credential type schema
        """
        return self._get(f"/api/v1/credentials/types/{credential_type}/schema")
    
    def validate(self, credential_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate credential configuration.
        
        Args:
            credential_type: The credential type
            config: The credential configuration to validate
            
        Returns:
            Validation result
        """
        return self._post(
            f"/api/v1/credentials/types/{credential_type}/validate",
            json_data=config,
        ) 