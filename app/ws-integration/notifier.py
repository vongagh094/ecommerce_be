"""WebSocket integration for sending notifications to clients."""

import json
import logging
import os
import requests
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class WebSocketNotifier:
    """WebSocket notification service that integrates with the ws-server."""
    
    def __init__(self):
        """Initialize the WebSocket notifier with configuration."""
        self.ws_server_url = os.environ.get("WS_SERVER_URL", "http://localhost:8080")
        self.enabled = bool(self.ws_server_url)
        if not self.enabled:
            logger.warning("WebSocket notifications disabled: WS_SERVER_URL not set")
    
    def send_to_user(self, user_id: int, message: Dict[str, Any]) -> bool:
        """Send a message to a specific user via WebSocket server.
        
        Args:
            user_id: The user ID to send the message to
            message: The message payload (must include 'type' field)
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        if not self.enabled:
            logger.debug(f"WebSocket disabled, would send to user {user_id}: {message}")
            return False
            
        if not isinstance(message, dict) or 'type' not in message:
            logger.error(f"Invalid WebSocket message format: {message}")
            return False
            
        try:
            # The ws-server exposes a REST API for sending messages
            endpoint = f"{self.ws_server_url}/push"
            payload = {
                "userId": str(user_id),
                "message": message
            }
            
            response = requests.post(
                endpoint, 
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=2  # Short timeout to avoid blocking
            )
            
            if response.status_code == 200:
                logger.debug(f"WebSocket message sent to user {user_id}: {message['type']}")
                return True
            else:
                logger.warning(f"Failed to send WebSocket message: {response.status_code} {response.text}")
                return False
                
        except Exception as e:
            logger.exception(f"Error sending WebSocket message: {e}")
            return False
    
    def broadcast(self, channel: str, message: Dict[str, Any]) -> bool:
        """Broadcast a message to a channel.
        
        Args:
            channel: The channel name (e.g., 'auction_results')
            message: The message payload (must include 'type' field)
            
        Returns:
            bool: True if message was broadcast successfully, False otherwise
        """
        if not self.enabled:
            logger.debug(f"WebSocket disabled, would broadcast to channel {channel}: {message}")
            return False
            
        if not isinstance(message, dict) or 'type' not in message:
            logger.error(f"Invalid WebSocket message format: {message}")
            return False
            
        try:
            # The ws-server exposes a REST API for broadcasting
            endpoint = f"{self.ws_server_url}/broadcast"
            payload = {
                "channel": channel,
                "message": message
            }
            
            response = requests.post(
                endpoint, 
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=2  # Short timeout to avoid blocking
            )
            
            if response.status_code == 200:
                logger.debug(f"WebSocket message broadcast to channel {channel}: {message['type']}")
                return True
            else:
                logger.warning(f"Failed to broadcast WebSocket message: {response.status_code} {response.text}")
                return False
                
        except Exception as e:
            logger.exception(f"Error broadcasting WebSocket message: {e}")
            return False 