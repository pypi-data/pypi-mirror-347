"""Computer class for interacting with Orgo virtual environments"""
# src/orgo/computer.py

import os
import io
import base64
from typing import Dict, List, Any, Optional, Callable, Union
from PIL import Image

from .api.client import ApiClient
from .prompt import get_provider


class Computer:
    def __init__(self, project_id=None, api_key=None, config=None, base_api_url=None):
        """
        Initialize an Orgo virtual computer.
        
        Args:
            project_id: Existing project ID to connect to (optional)
            api_key: Orgo API key (defaults to ORGO_API_KEY env var)
            config: Configuration for new computer (optional)
            base_api_url: Custom API URL (optional)
        """
        self.api_key = api_key or os.environ.get("ORGO_API_KEY")
        self.base_api_url = base_api_url
        self.api = ApiClient(self.api_key, self.base_api_url)
        
        if project_id:
            self.project_id = project_id
            self._info = self.api.connect_computer(project_id)
        else:
            response = self.api.create_computer(config)
            self.project_id = response.get("name")
            self._info = response
            
        if not self.project_id:
            raise ValueError("Failed to initialize computer: No project ID returned")
    
    def status(self) -> Dict[str, Any]:
        """Get current computer status"""
        return self.api.get_status(self.project_id)
    
    def restart(self) -> Dict[str, Any]:
        """Restart the computer"""
        return self.api.restart_computer(self.project_id)
    
    def shutdown(self) -> Dict[str, Any]:
        """Terminate the computer instance"""
        return self.api.shutdown_computer(self.project_id)
    
    # Navigation methods
    def left_click(self, x: int, y: int) -> Dict[str, Any]:
        """Perform left mouse click at specified coordinates"""
        return self.api.left_click(self.project_id, x, y)
    
    def right_click(self, x: int, y: int) -> Dict[str, Any]:
        """Perform right mouse click at specified coordinates"""
        return self.api.right_click(self.project_id, x, y)
    
    def double_click(self, x: int, y: int) -> Dict[str, Any]:
        """Perform double click at specified coordinates"""
        return self.api.double_click(self.project_id, x, y)
    
    def scroll(self, direction: str = "down", amount: int = 1) -> Dict[str, Any]:
        """Scroll in specified direction and amount"""
        return self.api.scroll(self.project_id, direction, amount)
    
    # Input methods
    def type(self, text: str) -> Dict[str, Any]:
        """Type the specified text"""
        return self.api.type_text(self.project_id, text)
    
    def key(self, key: str) -> Dict[str, Any]:
        """Press a key or key combination (e.g., "Enter", "ctrl+c")"""
        return self.api.key_press(self.project_id, key)
    
    # View methods
    def screenshot(self) -> Image.Image:
        """Capture screenshot and return as PIL Image"""
        response = self.api.get_screenshot(self.project_id)
        img_data = base64.b64decode(response.get("image", ""))
        return Image.open(io.BytesIO(img_data))
    
    def screenshot_base64(self) -> str:
        """Capture screenshot and return as base64 string"""
        response = self.api.get_screenshot(self.project_id)
        return response.get("image", "")
    
    # Execution methods
    def bash(self, command: str) -> str:
        """Execute a bash command and return output"""
        response = self.api.execute_bash(self.project_id, command)
        return response.get("output", "")
    
    def wait(self, seconds: float) -> Dict[str, Any]:
        """Wait for specified number of seconds"""
        return self.api.wait(self.project_id, seconds)
    
    # AI control method
    def prompt(self, 
               instruction: str,
               provider: str = "anthropic",
               model: str = "claude-3-7-sonnet-20250219",
               display_width: int = 1024,
               display_height: int = 768,
               callback: Optional[Callable[[str, Any], None]] = None,
               thinking_enabled: bool = False,
               thinking_budget: int = 1024,
               max_tokens: int = 4096,
               max_iterations: int = 20,
               max_saved_screenshots: int = 5,
               api_key: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Control the computer with natural language instructions using an AI assistant.
        
        Args:
            instruction: What you want the AI to do with the computer
            provider: AI provider to use (default: "anthropic")
            model: Model to use (default: "claude-3-7-sonnet-20250219")
            display_width: Screen width in pixels
            display_height: Screen height in pixels
            callback: Optional callback function for progress updates
            thinking_enabled: Enable Claude's thinking capability (default: False)
            thinking_budget: Token budget for thinking (default: 1024)
            max_tokens: Maximum tokens for model response
            max_iterations: Maximum number of agent loop iterations
            max_saved_screenshots: Maximum number of screenshots to keep in history (default: 5)
            api_key: API key for the AI provider (defaults to env var)
            
        Returns:
            List of messages from the conversation
            
        Examples:
            # Simple usage with environment variables
            computer.prompt("Open Firefox and search for Python tutorials")
            
            # With explicit API key
            computer.prompt("Open Terminal and list files", api_key="your-anthropic-key")
            
            # With callback for progress updates
            computer.prompt("Create a new text file", callback=my_callback_function)
            
            # With thinking enabled (Claude 3.7 Sonnet)
            computer.prompt(
                "Analyze a complex webpage", 
                thinking_enabled=True
            )
            
            # With custom screenshot management
            computer.prompt(
                "Perform a complex multi-step task",
                max_saved_screenshots=10  # Keep more screenshots for complex tasks
            )
        """
        # Get the provider instance
        provider_instance = get_provider(provider)
        
        # Execute the prompt
        return provider_instance.execute(
            computer_id=self.project_id,
            instruction=instruction,
            callback=callback,
            api_key=api_key,
            model=model,
            display_width=display_width,
            display_height=display_height,
            thinking_enabled=thinking_enabled,
            thinking_budget=thinking_budget,
            max_tokens=max_tokens,
            max_iterations=max_iterations,
            max_saved_screenshots=max_saved_screenshots,
            # Pass through the Orgo API client configuration
            orgo_api_key=self.api_key,
            orgo_base_url=self.base_api_url
        )