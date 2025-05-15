"""
Autonomous Routing Controller for the Zeebee AI Python SDK.

This module provides client-side access to the Autonomous Routing system,
allowing applications to intelligently route user messages to appropriate
agents, pipelines, or models based on detected intents and context.
"""

from typing import Dict, List, Any, Optional, Union
from .exceptions import RoutingException

class IntentCategory:
    """
    Available intent categories in the Zeebee AI routing system.
    
    This class provides constants for all supported intent categories,
    making code more readable and less error-prone when working with
    the routing system.
    """
    
    # Information seeking intents
    INFORMATION_RETRIEVAL = "INFORMATION_RETRIEVAL"
    
    # Content generation intents
    CONTENT_CREATION = "CONTENT_CREATION"
    CONTENT_SUMMARIZATION = "CONTENT_SUMMARIZATION"
    
    # Code-related intents
    CODE_GENERATION = "CODE_GENERATION"
    CODE_EXPLANATION = "CODE_EXPLANATION"
    
    # Analysis intents
    DATA_ANALYSIS = "DATA_ANALYSIS"
    SENTIMENT_ANALYSIS = "SENTIMENT_ANALYSIS"
    
    # Specialized intents
    TRANSLATION = "TRANSLATION"
    PERSONAL_ASSISTANCE = "PERSONAL_ASSISTANCE"
    CUSTOMER_SUPPORT = "CUSTOMER_SUPPORT"
    
    # System intents
    SYSTEM_INSTRUCTION = "SYSTEM_INSTRUCTION"
    
    # Fallback intent
    GENERAL_QUERY = "GENERAL_QUERY"
    
    # Unknown intent
    UNKNOWN = "UNKNOWN"
    
    @classmethod
    def all(cls) -> List[str]:
        """
        Returns a list of all available intent category values.
        
        Returns:
            List[str]: All available intent category values
        """
        return [
            cls.INFORMATION_RETRIEVAL,
            cls.CONTENT_CREATION,
            cls.CONTENT_SUMMARIZATION,
            cls.CODE_GENERATION,
            cls.CODE_EXPLANATION,
            cls.DATA_ANALYSIS,
            cls.SENTIMENT_ANALYSIS,
            cls.TRANSLATION,
            cls.PERSONAL_ASSISTANCE,
            cls.CUSTOMER_SUPPORT,
            cls.SYSTEM_INSTRUCTION,
            cls.GENERAL_QUERY,
            cls.UNKNOWN
        ]


class LayoutType:
    """
    Available layout types for the dynamic layout engine.
    
    This class provides constants for all supported layout types to use when
    requesting or specifying layout preferences.
    """
    
    # Simple text layout
    TEXT_HIGHLIGHT = "text-highlight"
    
    # List layouts
    CARD_LIST = "card-list"
    STACKED_CARDS = "stacked-cards"
    
    # Comparison layout
    COMPARISON_VIEW = "split"
    
    # Code display layout
    CODE_DISPLAY = "code"
    
    # Data visualization layout
    DATA_VISUALIZATION = "chart"
    
    # Document and story layouts
    STORY_BLOCK = "document"
    
    # Tabular data layout
    TABLE_LAYOUT = "dashboard"
    
    # Media gallery layout
    CAROUSEL_GALLERY = "media"
    
    # Timeline layout
    HERO_ALERT = "timeline"
    
    # Simple layout (default)
    SIMPLE = "simple"
    
    @classmethod
    def all(cls) -> List[str]:
        """
        Returns a list of all available layout type values.
        
        Returns:
            List[str]: All available layout type values
        """
        return [
            cls.TEXT_HIGHLIGHT,
            cls.CARD_LIST,
            cls.STACKED_CARDS,
            cls.COMPARISON_VIEW,
            cls.CODE_DISPLAY,
            cls.DATA_VISUALIZATION,
            cls.STORY_BLOCK,
            cls.TABLE_LAYOUT,
            cls.CAROUSEL_GALLERY,
            cls.HERO_ALERT,
            cls.SIMPLE
        ]


class RoutingController:
    """Controller for autonomous routing operations."""
    
    def __init__(self, client):
        """
        Initialize the routing controller.
        
        Args:
            client: ZeebeeClient instance
        """
        self.client = client
        
        # Validate that client session exists
        if not hasattr(self.client, '_session'):
            raise RoutingException("Client session not initialized. Make sure the ZeebeeClient is properly initialized.")
    
    def detect_intent(
        self,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Detect the intent from a user message.
        
        Args:
            message (str): The user message to analyze (required)
                Example: "How do I create a function in Python?"
                
            conversation_id (Optional[str]): Optional conversation ID for context
                If provided, the conversation history will be used to improve intent detection
                Example: "550e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Detected intent details including:
                - id: Intent ID
                - text: Original message
                - category: Intent category (one of IntentCategory values)
                - confidence: Confidence score (0.0-1.0)
                - timestamp: Detection timestamp
                - metadata: Additional intent information
            
        Raises:
            RoutingException: If validation fails or server returns an error
            
        Example:
            ```python
            intent = routing_controller.detect_intent(
                message="Can you write me a Python function to sort a list?",
                conversation_id="550e8400-e29b-41d4-a716-446655440000"
            )
            print(f"Detected intent: {intent['intent']['category']}")
            print(f"Confidence: {intent['intent']['confidence']}")
            ```
        """
        # Validate input data
        if not message:
            raise RoutingException("Message cannot be empty")
        
        if not isinstance(message, str):
            raise RoutingException("Message must be a string")
        
        if conversation_id is not None and not isinstance(conversation_id, str):
            raise RoutingException("Conversation ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/routing/detect-intent"
        
        payload = {
            "message": message
        }
        
        if conversation_id:
            payload["conversation_id"] = conversation_id
            
        try:
            response = self.client._session.post(
                endpoint,
                headers=self.client._get_headers(),
                json=payload,
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise RoutingException(f"Failed to detect intent: {e}")
    
    def route_message(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Route a user message to the appropriate agent, pipeline, or model.
        
        Args:
            message (str): The user message to route (required)
                Example: "Can you help me debug this code?"
                
            conversation_id (Optional[str]): Optional conversation ID for context
                If provided, the conversation history will be used to improve routing
                Example: "550e8400-e29b-41d4-a716-446655440000"
                
            context (Optional[Dict[str, Any]]): Additional context information
                Can include conversation history, user preferences, etc.
                Example: {
                    "history": [
                        {"role": "user", "content": "I'm working on a Python project"},
                        {"role": "assistant", "content": "Great! How can I help?"}
                    ],
                    "preferences": {
                        "preferred_models": ["gpt-4o", "claude-3-opus"]
                    }
                }
            
        Returns:
            Dict[str, Any]: Routing result including:
                - route_to: Name/ID of the agent, pipeline, or model
                - route_type: Type of route (agent, pipeline, model)
                - confidence: Confidence score (0.0-1.0)
                - intent: The detected intent
                - reasoning: Explanation of the routing decision
                - alternative_routes: List of alternative routing options
            
        Raises:
            RoutingException: If validation fails or server returns an error
            
        Example:
            ```python
            route = routing_controller.route_message(
                message="Can you help me debug this code?",
                conversation_id="550e8400-e29b-41d4-a716-446655440000"
            )
            print(f"Routing to: {route['route_to']} ({route['route_type']})")
            print(f"Confidence: {route['confidence']}")
            ```
        """
        # Validate input data
        if not message:
            raise RoutingException("Message cannot be empty")
        
        if not isinstance(message, str):
            raise RoutingException("Message must be a string")
        
        if conversation_id is not None and not isinstance(conversation_id, str):
            raise RoutingException("Conversation ID must be a string")
        
        if context is not None and not isinstance(context, dict):
            raise RoutingException("Context must be a dictionary")
        
        endpoint = f"{self.client.base_url}/api/routing/route"
        
        payload = {
            "message": message
        }
        
        if conversation_id:
            payload["conversation_id"] = conversation_id
            
        if context:
            payload["context"] = context
            
        try:
            response = self.client._session.post(
                endpoint,
                headers=self.client._get_headers(),
                json=payload,
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise RoutingException(f"Failed to route message: {e}")
    
    def provide_feedback(
        self,
        message: str,
        selected_route: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Provide feedback on a routing decision to improve future routing.
        
        Args:
            message (str): The original user message (required)
                Example: "Can you write me a Python function to sort a list?"
                
            selected_route (str): The route selected by the user (required)
                This should be the name/ID of an agent, pipeline, or model
                Example: "CodeAssistantAgent" or "gpt-4o"
                
            conversation_id (Optional[str]): Optional conversation ID for context
                Example: "550e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Feedback result
            
        Raises:
            RoutingException: If validation fails or server returns an error
            
        Example:
            ```python
            result = routing_controller.provide_feedback(
                message="Can you write me a Python function to sort a list?",
                selected_route="CodeAssistantAgent",
                conversation_id="550e8400-e29b-41d4-a716-446655440000"
            )
            print("Feedback provided successfully")
            ```
        """
        # Validate input data
        if not message:
            raise RoutingException("Message cannot be empty")
        
        if not isinstance(message, str):
            raise RoutingException("Message must be a string")
        
        if not selected_route:
            raise RoutingException("Selected route cannot be empty")
        
        if not isinstance(selected_route, str):
            raise RoutingException("Selected route must be a string")
        
        if conversation_id is not None and not isinstance(conversation_id, str):
            raise RoutingException("Conversation ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/routing/feedback"
        
        payload = {
            "message": message,
            "selected_route": selected_route
        }
        
        if conversation_id:
            payload["conversation_id"] = conversation_id
            
        try:
            response = self.client._session.post(
                endpoint,
                headers=self.client._get_headers(),
                json=payload,
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise RoutingException(f"Failed to provide feedback: {e}")
    
    def generate_layout(
        self,
        message: str,
        routing_result: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a dynamic layout based on message complexity and routing.
        
        Args:
            message (str): The user message to analyze (required)
                Example: "Can you create a table comparing different programming languages?"
                
            routing_result (Optional[Dict[str, Any]]): Optional routing result
                If provided, the layout will be customized based on the routing decision
                This should be the result from route_message()
                Example: {
                    "route_to": "StructureAgent",
                    "route_type": "agent",
                    "suggested_template": "table-layout",
                    "content_analysis": {
                        "contentTypes": ["table", "comparison"],
                        "complexity": "medium"
                    }
                }
            
        Returns:
            Dict[str, Any]: Layout configuration including:
                - template: Template name/type
                - components: List of UI components
                - styling: Styling information
                - visualization: Visualization settings
                - content_analysis: Analysis of content types and complexity
            
        Raises:
            RoutingException: If validation fails or server returns an error
            
        Example:
            ```python
            layout = routing_controller.generate_layout(
                message="Can you create a table comparing different programming languages?",
                routing_result={
                    "route_to": "StructureAgent",
                    "route_type": "agent",
                    "suggested_template": "table-layout"
                }
            )
            print(f"Generated layout template: {layout['layout']['template']}")
            print(f"Number of components: {len(layout['layout']['components'])}")
            ```
        """
        # Validate input data
        if not message:
            raise RoutingException("Message cannot be empty")
        
        if not isinstance(message, str):
            raise RoutingException("Message must be a string")
        
        if routing_result is not None and not isinstance(routing_result, dict):
            raise RoutingException("Routing result must be a dictionary")
        
        # During development/testing, use test endpoint
        endpoint = f"{self.client.base_url}/api/routing/test/layout"
        
        payload = {
            "message": message
        }
        
        if routing_result:
            payload["routing_result"] = routing_result
            
        try:
            response = self.client._session.post(
                endpoint,
                headers=self.client._get_headers(),
                json=payload,
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise RoutingException(f"Failed to generate layout: {e}")


class RoutingPipeline:
    """
    Utility class for building complete routing pipelines with intent detection, 
    routing and layout generation in a single workflow.
    """
    
    def __init__(self, routing_controller: RoutingController):
        """
        Initialize the routing pipeline.
        
        Args:
            routing_controller: RoutingController instance
        """
        self.routing_controller = routing_controller
    
    def process_message(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        generate_layout: bool = False,
        layout_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a message through the complete routing pipeline:
        1. Detect intent
        2. Route to appropriate destination
        3. Optionally generate layout
        
        Args:
            message (str): The user message to process (required)
                Example: "Can you create a table comparing different programming languages?"
                
            conversation_id (Optional[str]): Optional conversation ID for context
                Example: "550e8400-e29b-41d4-a716-446655440000"
                
            context (Optional[Dict[str, Any]]): Additional context information
                Example: {"history": [...], "preferences": {...}}
                
            generate_layout (bool): Whether to generate a layout
                Default: False
                
            layout_preferences (Optional[Dict[str, Any]]): Layout preferences
                Example: {
                    "suggested_template": "table-layout",
                    "content_analysis": {
                        "contentTypes": ["table", "comparison"],
                        "complexity": "medium"
                    }
                }
            
        Returns:
            Dict[str, Any]: Complete processing result including:
                - intent: The detected intent
                - routing: The routing result
                - layout: The generated layout (if requested)
            
        Raises:
            RoutingException: If any stage of processing fails
            
        Example:
            ```python
            result = routing_pipeline.process_message(
                message="Can you create a table comparing different programming languages?",
                conversation_id="550e8400-e29b-41d4-a716-446655440000",
                generate_layout=True,
                layout_preferences={"suggested_template": "table-layout"}
            )
            print(f"Intent category: {result['intent']['category']}")
            print(f"Routing to: {result['routing']['route_to']}")
            if 'layout' in result:
                print(f"Layout template: {result['layout']['template']}")
            ```
        """
        # Validate input data
        if not message:
            raise RoutingException("Message cannot be empty")
        
        if not isinstance(message, str):
            raise RoutingException("Message must be a string")
        
        # Step 1: Route the message (includes intent detection)
        routing_result = self.routing_controller.route_message(
            message=message,
            conversation_id=conversation_id,
            context=context
        )
        
        result = {
            "intent": routing_result.get("intent", {}),
            "routing": {
                "route_to": routing_result.get("route_to"),
                "route_type": routing_result.get("route_type"),
                "confidence": routing_result.get("confidence"),
                "alternative_routes": routing_result.get("alternative_routes", [])
            }
        }
        
        # Step 2: Generate layout if requested
        if generate_layout:
            # Create routing_result dict to pass to generate_layout
            layout_routing_result = {
                "route_to": routing_result.get("route_to"),
                "route_type": routing_result.get("route_type")
            }
            
            # Add any layout preferences provided
            if layout_preferences:
                layout_routing_result.update(layout_preferences)
            
            # Generate the layout
            layout_result = self.routing_controller.generate_layout(
                message=message,
                routing_result=layout_routing_result
            )
            
            # Add layout to result
            result["layout"] = layout_result.get("layout", {})
        
        return result
