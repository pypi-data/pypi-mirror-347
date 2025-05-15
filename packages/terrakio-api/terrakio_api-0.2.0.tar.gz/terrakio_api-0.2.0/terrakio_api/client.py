# This file is intentionally left empty.
# The Client class is now exposed via terrakio_api/__init__.py, which imports from terrakio_core.client.

import requests
import xarray as xr
from io import BytesIO
from typing import Dict, Any, Optional, Union
from typing import Dict, Any, Optional, Union

from .config import read_config_file, DEFAULT_CONFIG_FILE
from .exceptions import APIError, ConfigurationError
from .auth import AuthClient
from .user_management import UserManagement
from .dataset_management import DatasetManagement
from .dataset_management import DatasetManagement

from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry as ShapelyGeometry
from shapely.geometry.base import BaseGeometry as ShapelyGeometry
import json

class Client:
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None, 
                auth_url: Optional[str] = "https://dev-au.terrak.io",
                quiet: bool = False, config_file: Optional[str] = None,
                verify: bool = True, timeout: int = 60):
        """
        Initialize the Terrakio API client.
        
        Args:
            url: API base URL (optional, will use config file if not provided)
            key: API key or token (optional, will use config file if not provided)
            auth_url: Authentication API base URL (optional)
            quiet: If True, suppress progress messages
            config_file: Path to configuration file (default is $HOME/.tkio_config.json)
            verify: Verify SSL certificates
            timeout: Request timeout in seconds
        """
        self.quiet = quiet
        self.verify = verify
        self.timeout = timeout
        
        # Initialize authentication client
        self.auth_client = None
        if auth_url:
            self.auth_client = AuthClient(
                base_url=auth_url,
                verify=verify,
                timeout=timeout
            )
        
        # Initialize URL and key to None
        self.url = url
        self.key = key
        
        # Read from config file if either url or key is missing
        if self.url is None or self.key is None:
            if config_file is None:
                config_file = DEFAULT_CONFIG_FILE
            
            try:
                config = read_config_file(config_file)
                
                # Only use config values for missing parameters
                if self.url is None:
                    self.url = config.get('url')
                
                if self.key is None:
                    self.key = config.get('key')
                    
            except Exception as e:
                raise ConfigurationError(
                    f"Failed to read configuration: {e}\n\n"
                    "To fix this issue:\n"
                    "1. Create a file at ~/.terrakioapirc with:\n"
                    "url: https://api.terrak.io\n"
                    "key: your-api-key\n\n"
                    "OR\n\n"
                    "2. Initialize the client with explicit parameters:\n"
                    "client = terrakio_api.Client(\n"
                    "    url='https://api.terrak.io',\n"
                    "    key='your-api-key'\n"
                    ")"
                )
        
        # Validate configuration
        if not self.url:
            raise ConfigurationError("Missing API URL in configuration")
        if not self.key:
            raise ConfigurationError("Missing API key in configuration")
            
        # Ensure URL doesn't end with slash
        self.url = self.url.rstrip('/')
        
        if not self.quiet:
            print(f"Using Terrakio API at: {self.url}")
        
        # Initialize session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self.key
        })
        
        
    
    def validate_feature(self, feature: Dict[str, Any]) -> None:
        """
        Validate a GeoJSON feature using Shapely.
        
        Parameters:
        - feature: A GeoJSON feature dictionary or a Shapely geometry object
        - feature: A GeoJSON feature dictionary or a Shapely geometry object
        
        Raises:
        - ValueError: If the feature is invalid
        """
        # Check if the input is a Shapely geometry
        if hasattr(feature, 'is_valid'):
            # Convert Shapely geometry to GeoJSON feature
            from shapely.geometry import mapping
            feature = {
                "type": "Feature",
                "geometry": mapping(feature),
                "properties": {}
            }
        
        # Check if the input is a Shapely geometry
        if hasattr(feature, 'is_valid'):
            # Convert Shapely geometry to GeoJSON feature
            from shapely.geometry import mapping
            feature = {
                "type": "Feature",
                "geometry": mapping(feature),
                "properties": {}
            }
        
        # Check if the input is a valid GeoJSON feature
        if not isinstance(feature, dict):
            raise ValueError("Feature must be a dictionary or a Shapely geometry")
            raise ValueError("Feature must be a dictionary or a Shapely geometry")
        
        if feature.get("type") != "Feature":
            raise ValueError("GeoJSON object must be of type 'Feature'")
        
        if "geometry" not in feature:
            raise ValueError("Feature must contain a 'geometry' field")
        
        if "properties" not in feature:
            raise ValueError("Feature must contain a 'properties' field")
        
        # Convert to Shapely geometry and validate
        try:
            geometry = shape(feature["geometry"])
        except Exception as e:
            raise ValueError(f"Invalid geometry format: {str(e)}")
        
        # Use Shapely's validation capabilities
        if not geometry.is_valid:
            raise ValueError(f"Invalid geometry: {geometry.is_valid_reason}")
        
        # Additional validation based on geometry type
        geom_type = feature["geometry"]["type"]
        
        if geom_type == "Point":
            # Point-specific validation
            if len(feature["geometry"]["coordinates"]) != 2:
                raise ValueError("Point must have exactly 2 coordinates")
        
        elif geom_type == "Polygon":
            # Polygon-specific validation
            if not geometry.is_simple:
                raise ValueError("Polygon must be simple (not self-intersecting)")
            
            if geometry.area == 0:
                raise ValueError("Polygon must have non-zero area")
            
            # Check if the polygon is closed (first and last points match)
            coords = feature["geometry"]["coordinates"][0]
            if coords[0] != coords[-1]:
                raise ValueError("Polygon must be closed (first and last points must match)")
        
        # You can add more specific validation for other geometry types as needed
    
    def signup(self, email: str, password: str) -> Dict[str, Any]:
        """
        Register a new user account.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            API response data
        """
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
        
        return self.auth_client.signup(email, password)
    
    def login(self, email: str, password: str) -> str:
        """
        Authenticate with email and password to obtain a token.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Authentication token
        """
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
        
        token = self.auth_client.login(email, password)
        
        if not self.quiet:
            print(f"Successfully authenticated as: {email}")
            
        return token
    
    def refresh_api_key(self) -> str:

        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
            
        if not self.auth_client.token:
            raise ConfigurationError("Not authenticated. Call login() first.")
        
        self.key = self.auth_client.refresh_api_key()
        
        # Update session header with new API key
        self.session.headers.update({
            'x-api-key': self.key
        })
        
        # Write updated key to config file
        import json
        import os        

        config_path = os.path.join(os.environ.get("HOME", ""), ".tkio_config.json")
        
        try:
            # Default config if file doesn't exist
            config = {"EMAIL": "", "TERRAKIO_API_KEY": ""}
            
            # Try to read existing config if it exists
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
            
            # Update the API key
            config["TERRAKIO_API_KEY"] = self.key
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # Write back to the config file
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
                
            if not self.quiet:
                print(f"API key generated successfully and updated in {config_path}")
        except Exception as e:
            if not self.quiet:
                print(f"Warning: Failed to update config file: {e}")
        
        return self.key
        
    def view_api_key(self) -> str:
        """
        Retrieve current API key using authentication token.
        
        Returns:
            Current API key
        """
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
            
        if not self.auth_client.token:
            raise ConfigurationError("Not authenticated. Call login() first.")
        
        self.key = self.auth_client.view_api_key()
        
        # Update session header with retrieved API key
        self.session.headers.update({
            'x-api-key': self.key
        })
        
        return self.key
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Retrieve the current user's information.
        
        Returns:
            User information data
        """
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
            
        if not self.auth_client.token:
            raise ConfigurationError("Not authenticated. Call login() first.")
        
        return self.auth_client.get_user_info()
    
    def wcs(self, expr: str, feature: Union[Dict[str, Any], ShapelyGeometry], in_crs: str = "epsg:4326",
            out_crs: str = "epsg:4326", output: str = "csv", resolution: int = -1,
            **kwargs):
        """
        Make a WCS request to the Terrakio API.
        
        Args:
            expr: Expression string for data selection
            feature: GeoJSON Feature dictionary or a Shapely geometry object containing geometry information
            feature: GeoJSON Feature dictionary or a Shapely geometry object containing geometry information
            in_crs: Input coordinate reference system (default: "epsg:4326")
            out_crs: Output coordinate reference system (default: "epsg:4326")
            output: Output format (default: "csv")
            resolution: Resolution value (default: -1)
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            Data in the requested format (xr.Dataset for netcdf, pd.DataFrame for csv)
        """
        # Convert Shapely geometry to GeoJSON feature if needed
        if hasattr(feature, 'is_valid'):
            from shapely.geometry import mapping
            feature = {
                "type": "Feature",
                "geometry": mapping(feature),
                "properties": {}
            }
        # Convert Shapely geometry to GeoJSON feature if needed
        if hasattr(feature, 'is_valid'):
            from shapely.geometry import mapping
            feature = {
                "type": "Feature",
                "geometry": mapping(feature),
                "properties": {}
            }
        # Validate the feature object
        self.validate_feature(feature)
        
        # Prepare the payload
        payload = {
            "feature": feature,
            "in_crs": in_crs,
            "out_crs": out_crs,
            "output": output,
            "resolution": resolution,
            "expr": expr,
            **kwargs
        }
        
        if not self.quiet:
            print(f"Requesting data with expression: {expr}")
        request_url = f"{self.url}/wcs"
        try:
            # Make the API request
            
            response = self.session.post(request_url, json=payload, timeout=self.timeout, verify=self.verify)
            # Handle HTTP errors
            if not response.ok:
                error_msg = f"API request failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                
                raise APIError(error_msg)
            
            # Handle different output formats
            if output.lower() == "csv":
                import pandas as pd
                return pd.read_csv(BytesIO(response.content))
            elif output.lower() == "netcdf":
                return xr.open_dataset(BytesIO(response.content))
            else:
                # Try to determine the format and use appropriate reader
                try:
                    return xr.open_dataset(BytesIO(response.content))
                except ValueError:
                    import pandas as pd
                    try:
                        return pd.read_csv(BytesIO(response.content))
                    except:
                        # If all else fails, return the raw content
                        return response.content
            
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def get_user_by_id(self, user_id: str):
        if not hasattr(self, 'user_management') or self.user_management is None:
            from .user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.get_user_by_id(user_id)

    def get_user_by_email(self, email: str):
        if not hasattr(self, 'user_management') or self.user_management is None:
            from .user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.get_user_by_email(email)
    
    def list_users(self, substring: str = None, uid: bool = False):
        """
        List users, optionally filtering by a substring.
        
        Args:
            substring: Optional substring to filter users
            uid: If True, includes the user ID in the response (default: False)
            
        Returns:
            List of users
        """
        if not hasattr(self, 'user_management') or self.user_management is None:
            from .user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.list_users(substring=substring, uid=uid)

    def edit_user(
        self,
        user_id: str,
        uid: str = None,
        email: str = None,
        role: str = None,
        apiKey: str = None,
        groups: list = None,
        quota: int = None
    ):
        """
        Edit user info by user ID. Only provided fields will be updated.
        user_id is required.
        """
        if not hasattr(self, 'user_management') or self.user_management is None:
            from .user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.edit_user(
            user_id=user_id,
            uid=uid,
            email=email,
            role=role,
            apiKey=apiKey,
            groups=groups,
            quota=quota
        )
    
    def reset_quota(self, email: str, quota: int = None):
        if not hasattr(self, 'user_management') or self.user_management is None:
            from .user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.reset_quota(email=email, quota=quota)
    
    def delete_user(self, uid: str):
        if not hasattr(self, 'user_management') or self.user_management is None:
            from .user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.delete_user(uid=uid)

    def close(self):
        """Close the client session."""
        self.session.close()
        if self.auth_client:
            self.auth_client.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
