"""
Agent controller for the Zeebee AI Python SDK.
"""

from typing import Dict, List, Any, Optional
from .exceptions import AgentException

class AgentTypes:
    """
    Available agent types in the Zeebee AI platform.
    
    This class provides constants for all supported agent types to use when
    creating agents, making code more readable and less error-prone.
    """
    
    # Agent for retrieving information from knowledge bases
    RETRIEVAL = "RetrievalAgent"
    
    # Agent for summarizing long-form content
    SUMMARIZATION = "SummarizationAgent"
    
    # Agent for performing logical reasoning and analysis
    REASONING = "ReasoningAgent"
    
    # Agent for generating creative content
    GENERATION = "GenerationAgent"
    
    # Agent for interacting with web resources
    WEB = "WebAgent"
    
    # Agent for processing and transforming structured data
    STRUCTURE = "StructureAgent"
    
    @classmethod
    def all(cls) -> List[str]:
        """
        Returns a list of all available agent type names.
        
        Returns:
            List[str]: All available agent type names
        """
        return [
            cls.RETRIEVAL,
            cls.SUMMARIZATION, 
            cls.REASONING,
            cls.GENERATION,
            cls.WEB,
            cls.STRUCTURE
        ]

class AgentController:
    """Controller for agent operations."""
    
    def __init__(self, client):
        """
        Initialize the agent controller.
        
        Args:
            client: ZeebeeClient instance
        """
        self.client = client
        
        # Validate that client session exists
        if not hasattr(self.client, '_session'):
            raise AgentException("Client session not initialized. Make sure the ZeebeeClient is properly initialized.")
    
    def _validate_name(self, name: str) -> None:
        """
        Validate agent or pipeline name.
        
        Args:
            name: The name to validate
            
        Raises:
            AgentException: If validation fails
        """
        if not name:
            raise AgentException("Name cannot be empty")
        if not isinstance(name, str):
            raise AgentException("Name must be a string")
        if len(name) > 100:
            raise AgentException("Name is too long (maximum 100 characters)")
    
    def _validate_agent_type(self, agent_type: str) -> None:
        """
        Validate agent type.
        
        Args:
            agent_type: The agent type to validate
            
        Raises:
            AgentException: If validation fails
        """
        if not agent_type:
            raise AgentException("Agent type cannot be empty")
        if not isinstance(agent_type, str):
            raise AgentException("Agent type must be a string")
        if len(agent_type) > 50:
            raise AgentException("Agent type is too long (maximum 50 characters)")
    
    def _validate_dict(self, data: Dict[str, Any], field_name: str) -> None:
        """
        Validate a dictionary field.
        
        Args:
            data: The data to validate
            field_name: Name of the field for error messages
            
        Raises:
            AgentException: If validation fails
        """
        if not isinstance(data, dict):
            raise AgentException(f"{field_name} must be a dictionary")
    
    def _validate_optional_string(self, value: Optional[str], field_name: str, max_length: int = 255) -> None:
        """
        Validate an optional string field.
        
        Args:
            value: The value to validate
            field_name: Name of the field for error messages
            max_length: Maximum length of the string
            
        Raises:
            AgentException: If validation fails
        """
        if value is not None:
            if not isinstance(value, str):
                raise AgentException(f"{field_name} must be a string")
            if len(value) > max_length:
                raise AgentException(f"{field_name} is too long (maximum {max_length} characters)")
    
    def _validate_stages(self, stages: List[Dict[str, Any]]) -> None:
        """
        Validate pipeline stages.
        
        Args:
            stages: List of stage configurations to validate
            
        Raises:
            AgentException: If validation fails
        """
        if not isinstance(stages, list):
            raise AgentException("Stages must be a list")
        
        for i, stage in enumerate(stages):
            if not isinstance(stage, dict):
                raise AgentException(f"Stage {i+1} must be a dictionary")
            
            if 'agent_id' not in stage:
                raise AgentException(f"Stage {i+1} is missing required field 'agent_id'")
            
            if not isinstance(stage.get('agent_id'), str):
                raise AgentException(f"Stage {i+1} 'agent_id' must be a string")
                
            # Validate optional fields if present
            if 'name' in stage and not isinstance(stage['name'], str):
                raise AgentException(f"Stage {i+1} 'name' must be a string")
                
            if 'input_mapping' in stage and not isinstance(stage['input_mapping'], dict):
                raise AgentException(f"Stage {i+1} 'input_mapping' must be a dictionary")
                
            if 'output_mapping' in stage and not isinstance(stage['output_mapping'], dict):
                raise AgentException(f"Stage {i+1} 'output_mapping' must be a dictionary")
                
            if 'condition' in stage and not isinstance(stage['condition'], dict):
                raise AgentException(f"Stage {i+1} 'condition' must be a dictionary")
    
    def create_agent(
        self,
        name: str,
        agent_type: str,
        configuration: Dict[str, Any],
        description: Optional[str] = None,
        model_id: Optional[str] = None,
        is_public: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new agent.
        
        Args:
            name (str): Name of the agent to create (required)
                Example: "Web Search Agent"
            
            agent_type (str): Type of agent to create (required)
                Available types can be retrieved using get_agent_types()
                Example: "WebAgent", "StructureAgent"
            
            configuration (Dict[str, Any]): Configuration settings for the agent (required)
                The structure depends on the agent type
                Example: {"base_url": "https://example.com", "api_key": "your-api-key"}
            
            description (Optional[str]): Optional description of the agent's purpose
                Example: "Agent for searching the web for information"
            
            model_id (Optional[str]): ID of the LLM model to use with this agent
                If not provided, the system default will be used
                Example: "gpt-4o" or the UUID of a model in the system
            
            is_public (bool): Whether the agent should be accessible to other users
                Default: False (private to the creator)
            
        Returns:
            Dict[str, Any]: Created agent details including its ID
            
        Raises:
            AgentException: If validation fails or server returns an error
            
        Example:
            ```python
            agent = agent_controller.create_agent(
                name="Web Search Agent",
                agent_type="WebAgent",
                configuration={
                    "search_engine": "google",
                    "num_results": 5
                },
                description="Agent for searching the web for information",
                model_id="gpt-4o"
            )
            print(f"Created agent with ID: {agent['id']}")
            ```
        """
        # Validate input data
        self._validate_name(name)
        self._validate_agent_type(agent_type)
        self._validate_dict(configuration, "Configuration")
        self._validate_optional_string(description, "Description", 1000)
        self._validate_optional_string(model_id, "Model ID", 100)
        
        if not isinstance(is_public, bool):
            raise AgentException("is_public must be a boolean")
        
        endpoint = f"{self.client.base_url}/api/agent/agents"
        
        payload = {
            "name": name,
            "agent_type": agent_type,
            "configuration": configuration,
        }
        
        if description:
            payload["description"] = description
            
        if model_id is not None:
            payload["model_id"] = model_id
            
        if is_public is not None:
            payload["is_public"] = is_public
            
        try:
            if not hasattr(self.client, '_session'):
                raise AgentException("Client session not available")
                
            response = self.client._session.post(
                endpoint,
                headers=self.client._get_headers(),
                json=payload,
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to create agent: {e}")
    
    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Get agent details by ID.
        
        Args:
            agent_id (str): The unique identifier of the agent to retrieve (required)
                This is the ID returned when creating an agent
                Example: "550e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Agent details including configuration and metadata
            
        Raises:
            AgentException: If validation fails, agent doesn't exist, or server returns an error
            
        Example:
            ```python
            agent = agent_controller.get_agent("550e8400-e29b-41d4-a716-446655440000")
            print(f"Agent name: {agent['name']}")
            print(f"Agent type: {agent['agent_type']}")
            ```
        """
        # Validate input data
        if not agent_id:
            raise AgentException("Agent ID cannot be empty")
        
        if not isinstance(agent_id, str):
            raise AgentException("Agent ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/agents/{agent_id}"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to get agent: {e}")
    
    def update_agent(
        self,
        agent_id: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing agent.
        
        Args:
            agent_id (str): The unique identifier of the agent to update (required)
                Example: "550e8400-e29b-41d4-a716-446655440000"
                
            update_data (Dict[str, Any]): Data to update on the agent (required)
                Only include fields you want to modify
                Supported fields:
                - name: New name for the agent
                - description: New description
                - configuration: Updated configuration dictionary
                - model_id: New model ID to use
                - is_public: Change visibility status
                
                Example: {"name": "New Agent Name", "configuration": {"new_config": "value"}}
            
        Returns:
            Dict[str, Any]: Updated agent details
            
        Raises:
            AgentException: If validation fails, agent doesn't exist, you don't have 
                           permission to update it, or server returns an error
            
        Example:
            ```python
            updated_agent = agent_controller.update_agent(
                agent_id="550e8400-e29b-41d4-a716-446655440000",
                update_data={
                    "name": "Improved Web Agent",
                    "configuration": {"search_engine": "bing", "num_results": 10}
                }
            )
            print("Agent updated successfully")
            ```
        """
        # Validate input data
        if not agent_id:
            raise AgentException("Agent ID cannot be empty")
        
        if not isinstance(agent_id, str):
            raise AgentException("Agent ID must be a string")
        
        if not isinstance(update_data, dict):
            raise AgentException("Update data must be a dictionary")
        
        # Validate fields in update_data if they exist
        if 'name' in update_data:
            self._validate_name(update_data['name'])
            
        if 'description' in update_data:
            self._validate_optional_string(update_data['description'], "Description", 1000)
            
        if 'configuration' in update_data:
            self._validate_dict(update_data['configuration'], "Configuration")
            
        if 'model_id' in update_data and update_data['model_id'] is not None:
            self._validate_optional_string(update_data['model_id'], "Model ID", 100)
            
        if 'is_public' in update_data and not isinstance(update_data['is_public'], bool):
            raise AgentException("is_public must be a boolean")
        
        endpoint = f"{self.client.base_url}/api/agent/agents/{agent_id}"
        
        try:
            response = self.client._session.put(
                endpoint,
                headers=self.client._get_headers(),
                json=update_data,
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to update agent: {e}")
    
    def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Delete an agent.
        
        Args:
            agent_id (str): The unique identifier of the agent to delete (required)
                Example: "550e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Deletion confirmation
            
        Raises:
            AgentException: If validation fails, agent doesn't exist, you don't have 
                           permission to delete it, or server returns an error
            
        Example:
            ```python
            result = agent_controller.delete_agent("550e8400-e29b-41d4-a716-446655440000")
            print("Agent deleted successfully")
            ```
        """
        # Validate input data
        if not agent_id:
            raise AgentException("Agent ID cannot be empty")
        
        if not isinstance(agent_id, str):
            raise AgentException("Agent ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/agents/{agent_id}"
        
        try:
            response = self.client._session.delete(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to delete agent: {e}")
            
    def execute_agent(
        self,
        agent_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute an agent with the provided input data.
        
        Args:
            agent_id (str): The unique identifier of the agent to execute (required)
                Example: "550e8400-e29b-41d4-a716-446655440000"
                
            input_data (Dict[str, Any]): Input data for the agent to process (required)
                The structure depends on the agent type
                Example for WebAgent: {"query": "What is the weather in New York?"}
                Example for StructureAgent: {"text": "Extract data from this text..."}
            
        Returns:
            Dict[str, Any]: Agent execution result
                The structure depends on the agent type
            
        Raises:
            AgentException: If validation fails, agent doesn't exist, you don't have 
                           permission to execute it, or server returns an error
            
        Example:
            ```python
            result = agent_controller.execute_agent(
                agent_id="550e8400-e29b-41d4-a716-446655440000",
                input_data={"query": "What is the weather in New York?"}
            )
            print(f"Agent response: {result['result']}")
            ```
        """
        # Validate input data
        if not agent_id:
            raise AgentException("Agent ID cannot be empty")
        
        if not isinstance(agent_id, str):
            raise AgentException("Agent ID must be a string")
        
        if not isinstance(input_data, dict):
            raise AgentException("Input data must be a dictionary")
        
        endpoint = f"{self.client.base_url}/api/agent/agents/{agent_id}/execute"
        
        try:
            response = self.client._session.post(
                endpoint,
                headers=self.client._get_headers(),
                json=input_data,
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to execute agent: {e}")
            
    def get_agent_types(self) -> Dict[str, Any]:
        """
        Get all available agent types.
        
        Returns:
            Dict[str, Any]: List of available agent types with their descriptions
            
        Raises:
            AgentException: If server returns an error
            
        Example:
            ```python
            agent_types = agent_controller.get_agent_types()
            print("Available agent types:")
            for agent_type in agent_types["agent_types"]:
                print(f"- {agent_type}")
            ```
        """
        endpoint = f"{self.client.base_url}/api/agent/types"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to get agent types: {e}")
            
    def get_agents(self) -> Dict[str, Any]:
        """
        Get all agents available to the user.
        
        Returns:
            Dict[str, Any]: List of available agents with their metadata
                Includes both agents created by the user and public agents
            
        Raises:
            AgentException: If server returns an error
            
        Example:
            ```python
            agents = agent_controller.get_agents()
            print("My agents:")
            for agent in agents["agents"]:
                print(f"- {agent['name']} (ID: {agent['id']})")
            ```
        """
        endpoint = f"{self.client.base_url}/api/agent/agents"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to get agents: {e}")
            
    # Pipeline methods
    def create_pipeline(
        self,
        name: str,
        stages: Optional[List[Dict[str, Any]]] = None,
        description: Optional[str] = None,
        visual_layout: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new pipeline of connected agents.
        
        Args:
            name (str): Name of the pipeline to create (required)
                Example: "Web Search and Summarize Pipeline"
                
            stages (Optional[List[Dict[str, Any]]]): List of pipeline stages
                Each stage is a dictionary with these fields:
                - agent_id: ID of the agent to use (required)
                - name: Name for this stage (optional)
                - input_mapping: How to map pipeline inputs to agent inputs (optional)
                - output_mapping: How to map agent outputs to pipeline outputs (optional)
                - condition: Conditions for when to run this stage (optional)
                
                Example: [
                    {
                        "agent_id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Web Search",
                        "input_mapping": {"query": "$.input.search_query"},
                        "output_mapping": {"search_results": "$.output.results"}
                    },
                    {
                        "agent_id": "661f9511-f3ab-52e5-b827-557766551111",
                        "name": "Summarize",
                        "input_mapping": {"text": "$.stages.Web Search.search_results"},
                        "output_mapping": {"summary": "$.output.summary"}
                    }
                ]
                
            description (Optional[str]): Optional description of the pipeline's purpose
                Example: "Pipeline that searches the web and summarizes the results"
                
            visual_layout (Optional[Dict[str, Any]]): Optional visual layout information
                Used by the visual pipeline builder interface
                Example: {"nodes": [...], "edges": [...]}
            
        Returns:
            Dict[str, Any]: Created pipeline details including its ID
            
        Raises:
            AgentException: If validation fails or server returns an error
            
        Example:
            ```python
            pipeline = agent_controller.create_pipeline(
                name="Search and Summarize",
                stages=[
                    {
                        "agent_id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Web Search",
                        "input_mapping": {"query": "$.input.search_query"},
                        "output_mapping": {"search_results": "$.output.results"}
                    },
                    {
                        "agent_id": "661f9511-f3ab-52e5-b827-557766551111",
                        "name": "Summarize",
                        "input_mapping": {"text": "$.stages.Web Search.search_results"},
                        "output_mapping": {"summary": "$.output.summary"}
                    }
                ],
                description="Pipeline that searches the web and summarizes the results"
            )
            print(f"Created pipeline with ID: {pipeline['pipeline_id']}")
            ```
        """
        # Validate input data
        self._validate_name(name)
        self._validate_optional_string(description, "Description", 1000)
        
        if stages is not None:
            self._validate_stages(stages)
        
        if visual_layout is not None:
            self._validate_dict(visual_layout, "Visual layout")
        
        endpoint = f"{self.client.base_url}/api/agent/pipelines"
        
        payload = {
            "name": name
        }
        
        if description:
            payload["description"] = description
            
        if stages:
            payload["stages"] = stages
            
        if visual_layout:
            payload["visual_layout"] = visual_layout
            
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
            raise AgentException(f"Failed to create pipeline: {e}")
            
    def get_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get pipeline details by ID.
        
        Args:
            pipeline_id (str): The unique identifier of the pipeline to retrieve (required)
                Example: "770e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Pipeline details including stages, configuration and metadata
            
        Raises:
            AgentException: If validation fails, pipeline doesn't exist, or server returns an error
            
        Example:
            ```python
            pipeline = agent_controller.get_pipeline("770e8400-e29b-41d4-a716-446655440000")
            print(f"Pipeline name: {pipeline['pipeline']['name']}")
            print(f"Number of stages: {len(pipeline['pipeline']['configuration']['stages'])}")
            ```
        """
        # Validate input data
        if not pipeline_id:
            raise AgentException("Pipeline ID cannot be empty")
        
        if not isinstance(pipeline_id, str):
            raise AgentException("Pipeline ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/pipelines/{pipeline_id}"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to get pipeline: {e}")
            
    def update_pipeline(
        self,
        pipeline_id: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing pipeline.
        
        Args:
            pipeline_id (str): The unique identifier of the pipeline to update (required)
                Example: "770e8400-e29b-41d4-a716-446655440000"
                
            update_data (Dict[str, Any]): Data to update on the pipeline (required)
                Only include fields you want to modify
                Supported fields:
                - name: New name for the pipeline
                - description: New description
                - stages: Updated list of pipeline stages
                - visual_layout: Updated visual layout information
                
                Example: {"name": "New Pipeline Name", "stages": [...]}
            
        Returns:
            Dict[str, Any]: Updated pipeline details
            
        Raises:
            AgentException: If validation fails, pipeline doesn't exist, you don't have 
                           permission to update it, or server returns an error
            
        Example:
            ```python
            updated_pipeline = agent_controller.update_pipeline(
                pipeline_id="770e8400-e29b-41d4-a716-446655440000",
                update_data={
                    "name": "Improved Search and Summarize",
                    "stages": [
                        # Updated stages configuration...
                    ]
                }
            )
            print("Pipeline updated successfully")
            ```
        """
        # Validate input data
        if not pipeline_id:
            raise AgentException("Pipeline ID cannot be empty")
        
        if not isinstance(pipeline_id, str):
            raise AgentException("Pipeline ID must be a string")
        
        if not isinstance(update_data, dict):
            raise AgentException("Update data must be a dictionary")
        
        # Validate fields in update_data if they exist
        if 'name' in update_data:
            self._validate_name(update_data['name'])
            
        if 'description' in update_data:
            self._validate_optional_string(update_data['description'], "Description", 1000)
            
        if 'stages' in update_data:
            self._validate_stages(update_data['stages'])
            
        if 'visual_layout' in update_data:
            self._validate_dict(update_data['visual_layout'], "Visual layout")
        
        endpoint = f"{self.client.base_url}/api/agent/pipelines/{pipeline_id}"
        
        try:
            response = self.client._session.put(
                endpoint,
                headers=self.client._get_headers(),
                json=update_data,
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to update pipeline: {e}")
            
    def delete_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Delete a pipeline.
        
        Args:
            pipeline_id (str): The unique identifier of the pipeline to delete (required)
                Example: "770e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Deletion confirmation
            
        Raises:
            AgentException: If validation fails, pipeline doesn't exist, you don't have 
                           permission to delete it, or server returns an error
            
        Example:
            ```python
            result = agent_controller.delete_pipeline("770e8400-e29b-41d4-a716-446655440000")
            print("Pipeline deleted successfully")
            ```
        """
        # Validate input data
        if not pipeline_id:
            raise AgentException("Pipeline ID cannot be empty")
        
        if not isinstance(pipeline_id, str):
            raise AgentException("Pipeline ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/pipelines/{pipeline_id}"
        
        try:
            response = self.client._session.delete(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to delete pipeline: {e}")
            
    def execute_pipeline(
        self,
        pipeline_id: str,
        input_data: Dict[str, Any],
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a pipeline with the provided input data.
        
        Args:
            pipeline_id (str): The unique identifier of the pipeline to execute (required)
                Example: "770e8400-e29b-41d4-a716-446655440000"
                
            input_data (Dict[str, Any]): Input data for the pipeline to process (required)
                The structure depends on the pipeline's input_mapping configuration
                Example: {"search_query": "What is the capital of France?"}
                
            conversation_id (Optional[str]): Optional conversation ID to link this execution to
                If provided, the execution will be associated with the conversation
                Example: "990e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Pipeline execution result
                Contains the final output of the pipeline and execution metadata
            
        Raises:
            AgentException: If validation fails, pipeline doesn't exist, you don't have 
                           permission to execute it, or server returns an error
            
        Example:
            ```python
            result = agent_controller.execute_pipeline(
                pipeline_id="770e8400-e29b-41d4-a716-446655440000",
                input_data={"search_query": "What is the capital of France?"}
            )
            print(f"Pipeline result: {result['result']}")
            ```
        """
        # Validate input data
        if not pipeline_id:
            raise AgentException("Pipeline ID cannot be empty")
        
        if not isinstance(pipeline_id, str):
            raise AgentException("Pipeline ID must be a string")
        
        if not isinstance(input_data, dict):
            raise AgentException("Input data must be a dictionary")
        
        if conversation_id is not None and not isinstance(conversation_id, str):
            raise AgentException("Conversation ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/pipelines/{pipeline_id}/execute"
        
        payload = input_data.copy()
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
            raise AgentException(f"Failed to execute pipeline: {e}")
            
    def get_pipeline_executions(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get all executions of a pipeline.
        
        Args:
            pipeline_id (str): The unique identifier of the pipeline (required)
                Example: "770e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: List of pipeline executions with their status and metadata
            
        Raises:
            AgentException: If validation fails, pipeline doesn't exist, you don't have 
                           permission to access it, or server returns an error
            
        Example:
            ```python
            executions = agent_controller.get_pipeline_executions("770e8400-e29b-41d4-a716-446655440000")
            print(f"Found {len(executions['executions'])} execution(s):")
            for execution in executions['executions']:
                print(f"- ID: {execution['id']}, Status: {execution['status']}")
            ```
        """
        # Validate input data
        if not pipeline_id:
            raise AgentException("Pipeline ID cannot be empty")
        
        if not isinstance(pipeline_id, str):
            raise AgentException("Pipeline ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/pipelines/{pipeline_id}/executions"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to get pipeline executions: {e}")
            
    def get_execution(self, execution_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific pipeline execution.
        
        Args:
            execution_id (str): The unique identifier of the execution to retrieve (required)
                Example: "880e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Detailed execution information including:
                - Status
                - Input/output data
                - Execution time
                - Stage-by-stage execution details
                - Error messages (if any)
            
        Raises:
            AgentException: If validation fails, execution doesn't exist, you don't have 
                           permission to access it, or server returns an error
            
        Example:
            ```python
            execution = agent_controller.get_execution("880e8400-e29b-41d4-a716-446655440000")
            print(f"Execution status: {execution['execution']['status']}")
            print(f"Total execution time: {execution['execution']['execution_time_ms']}ms")
            print("Stage results:")
            for stage in execution['execution']['stages']:
                print(f"- {stage['stage_name']}: {stage['status']}")
            ```
        """
        # Validate input data
        if not execution_id:
            raise AgentException("Execution ID cannot be empty")
        
        if not isinstance(execution_id, str):
            raise AgentException("Execution ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/executions/{execution_id}"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to get execution: {e}")
