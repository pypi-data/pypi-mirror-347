"""
Module with base command class.
"""

import inspect
from abc import ABC, abstractmethod
from typing import Any, ClassVar, Dict, List, Optional, Type, TypeVar, Union

from mcp_proxy_adapter.commands.result import CommandResult, ErrorResult, SuccessResult
from mcp_proxy_adapter.core.errors import (
    ValidationError, CommandError, InternalError, InvalidParamsError, 
    NotFoundError, TimeoutError
)
from mcp_proxy_adapter.core.logging import logger

T = TypeVar("T", bound=CommandResult)


class Command(ABC):
    """
    Base abstract class for all commands.
    """
    
    # Command name for registration
    name: ClassVar[str]
    # Result class
    result_class: ClassVar[Type[CommandResult]]
    
    @abstractmethod
    async def execute(self, **kwargs) -> CommandResult:
        """
        Executes command with given parameters.

        Args:
            **kwargs: Command parameters.

        Returns:
            Command execution result.
        """
        pass
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Returns JSON schema for command parameters validation.
        This method should be overridden in child classes.

        Returns:
            Dictionary with JSON schema.
        """
        # Default base schema that can be overridden
        return {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    
    @classmethod
    def get_result_schema(cls) -> Dict[str, Any]:
        """
        Returns JSON schema for command result validation.

        Returns:
            Dictionary with JSON schema.
        """
        if hasattr(cls, "result_class") and cls.result_class:
            return cls.result_class.get_schema()
        return {}
    
    @classmethod
    def validate_params(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates command parameters before execution.
        This method can be overridden in child classes for custom validation.

        Args:
            params: Parameters to validate.

        Returns:
            Validated parameters.

        Raises:
            ValidationError: If parameters failed validation.
        """
        # In base implementation, simply return parameters without validation
        # In real implementation, jsonschema or pydantic will be used here
        return params
    
    @classmethod
    async def run(cls, **kwargs) -> CommandResult:
        """
        Runs command with parameters validation.

        Args:
            **kwargs: Command parameters.

        Returns:
            Command execution result.
        """
        try:
            logger.debug(f"Running command {cls.__name__} with params: {kwargs}")
            
            # Import registry here to avoid circular imports
            from mcp_proxy_adapter.commands.command_registry import registry
            
            # Get command name
            if not hasattr(cls, "name") or not cls.name:
                command_name = cls.__name__.lower()
                if command_name.endswith("command"):
                    command_name = command_name[:-7]
            else:
                command_name = cls.name
                
            # Parameters validation
            validated_params = cls.validate_params(kwargs)
            
            # Check if we have a registered instance for this command
            if registry.has_instance(command_name):
                # Use existing instance with dependencies
                command = registry.get_command_instance(command_name)
                result = await command.execute(**validated_params)
            else:
                # Create new instance for commands without dependencies
                command = cls()
                result = await command.execute(**validated_params)
            
            logger.debug(f"Command {cls.__name__} executed successfully")
            return result
        except ValidationError as e:
            # Ошибка валидации параметров
            logger.error(f"Validation error in command {cls.__name__}: {e}")
            return ErrorResult(
                message=str(e), 
                code=e.code, 
                details=e.data
            )
        except InvalidParamsError as e:
            # Ошибка в параметрах команды
            logger.error(f"Invalid parameters error in command {cls.__name__}: {e}")
            return ErrorResult(
                message=str(e), 
                code=e.code, 
                details=e.data
            )
        except NotFoundError as e:
            # Ресурс не найден
            logger.error(f"Resource not found error in command {cls.__name__}: {e}")
            return ErrorResult(
                message=str(e), 
                code=e.code, 
                details=e.data
            )
        except TimeoutError as e:
            # Превышено время ожидания
            logger.error(f"Timeout error in command {cls.__name__}: {e}")
            return ErrorResult(
                message=str(e), 
                code=e.code, 
                details=e.data
            )
        except CommandError as e:
            # Ошибка выполнения команды
            logger.error(f"Command error in {cls.__name__}: {e}")
            return ErrorResult(
                message=str(e), 
                code=e.code, 
                details=e.data
            )
        except Exception as e:
            # Непредвиденная ошибка
            logger.exception(f"Unexpected error executing command {cls.__name__}: {e}")
            internal_error = InternalError(f"Command execution error: {str(e)}")
            return ErrorResult(
                message=internal_error.message,
                code=internal_error.code,
                details={"original_error": str(e)}
            )
    
    @classmethod
    def get_param_info(cls) -> Dict[str, Dict[str, Any]]:
        """
        Gets information about execute method parameters.

        Returns:
            Dictionary with parameters information.
        """
        signature = inspect.signature(cls.execute)
        params = {}
        
        for name, param in signature.parameters.items():
            if name == "self":
                continue
                
            param_info = {
                "name": name,
                "required": param.default == inspect.Parameter.empty
            }
            
            if param.annotation != inspect.Parameter.empty:
                param_info["type"] = str(param.annotation)
            
            if param.default != inspect.Parameter.empty:
                param_info["default"] = param.default
                
            params[name] = param_info
            
        return params
    
    @classmethod
    def get_metadata(cls) -> Dict[str, Any]:
        """
        Returns complete metadata about the command.
        
        Provides a single access point to all command metadata.
        
        Returns:
            Dict with command metadata
        """
        # Get and format docstring
        doc = cls.__doc__ or ""
        description = inspect.cleandoc(doc) if doc else ""
        
        # Extract first line for summary
        summary = description.split("\n")[0] if description else ""
        
        # Get parameters information
        param_info = cls.get_param_info()
        
        # Generate examples based on parameters
        examples = cls._generate_examples(param_info)
        
        return {
            "name": cls.name,
            "summary": summary,
            "description": description,
            "params": param_info,
            "examples": examples,
            "schema": cls.get_schema(),
            "result_schema": cls.get_result_schema(),
            "result_class": cls.result_class.__name__ if hasattr(cls, "result_class") else None,
        }
    
    @classmethod
    def _generate_examples(cls, params: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generates usage examples of the command based on its parameters.
        
        Args:
            params: Information about command parameters
            
        Returns:
            List of examples
        """
        examples = []
        
        # Simple example without parameters, if all parameters are optional
        if not any(param.get("required", False) for param in params.values()):
            examples.append({
                "command": cls.name,
                "description": f"Call {cls.name} command without parameters"
            })
        
        # Example with all required parameters
        required_params = {k: v for k, v in params.items() if v.get("required", False)}
        if required_params:
            sample_params = {}
            for param_name, param_info in required_params.items():
                # Try to generate sample value based on type
                param_type = param_info.get("type", "")
                
                if "str" in param_type:
                    sample_params[param_name] = f"sample_{param_name}"
                elif "int" in param_type:
                    sample_params[param_name] = 1
                elif "float" in param_type:
                    sample_params[param_name] = 1.0
                elif "bool" in param_type:
                    sample_params[param_name] = True
                elif "list" in param_type or "List" in param_type:
                    sample_params[param_name] = []
                elif "dict" in param_type or "Dict" in param_type:
                    sample_params[param_name] = {}
                else:
                    sample_params[param_name] = "..."
            
            examples.append({
                "command": cls.name,
                "params": sample_params,
                "description": f"Call {cls.name} command with required parameters"
            })
            
        # Example with all parameters (including optional ones)
        if len(params) > len(required_params):
            all_params = {}
            for param_name, param_info in params.items():
                # For required parameters, use the same values as above
                if param_info.get("required", False):
                    # Try to generate sample value based on type
                    param_type = param_info.get("type", "")
                    
                    if "str" in param_type:
                        all_params[param_name] = f"sample_{param_name}"
                    elif "int" in param_type:
                        all_params[param_name] = 1
                    elif "float" in param_type:
                        all_params[param_name] = 1.0
                    elif "bool" in param_type:
                        all_params[param_name] = True
                    elif "list" in param_type or "List" in param_type:
                        all_params[param_name] = []
                    elif "dict" in param_type or "Dict" in param_type:
                        all_params[param_name] = {}
                    else:
                        all_params[param_name] = "..."
                # For optional parameters, use their default values or a sample value
                else:
                    if "default" in param_info:
                        all_params[param_name] = param_info["default"]
                    else:
                        # Generate based on type
                        param_type = param_info.get("type", "")
                        
                        if "str" in param_type:
                            all_params[param_name] = f"optional_{param_name}"
                        elif "int" in param_type:
                            all_params[param_name] = 42
                        elif "float" in param_type:
                            all_params[param_name] = 3.14
                        elif "bool" in param_type:
                            all_params[param_name] = False
                        elif "list" in param_type or "List" in param_type:
                            all_params[param_name] = ["sample"]
                        elif "dict" in param_type or "Dict" in param_type:
                            all_params[param_name] = {"key": "value"}
                        else:
                            all_params[param_name] = "sample_value"
            
            examples.append({
                "command": cls.name,
                "params": all_params,
                "description": f"Call {cls.name} command with all parameters"
            })
        
        return examples