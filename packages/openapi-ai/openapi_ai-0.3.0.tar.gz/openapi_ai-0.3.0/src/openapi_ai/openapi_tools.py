from typing import Any
from agents import RunContextWrapper, FunctionTool
from .generator import generate_tools

class OpenAPITools:
    """
    A class to generate Python functions for OpenAPI endpoints and to create
    OpenAI FunctionTool objects from the endpoints.

    The class takes a URL to an OpenAPI specification file and an optional
    remove_prefix argument to remove a prefix from the endpoint paths when
    generating function names. The functions are generated using the
    generate_tools function from the generator module.

    The class has two methods: get_function_tools and get_openai_tools. The
    first method returns a dictionary of all the generated endpoint functions.
    The second method generates a list of OpenAI FunctionTool objects from the
    endpoints. Each endpoint is converted into a FunctionTool, which is a
    callable object with a name, description, JSON schema for parameters, and a
    function that will be called when the tool is invoked.

    Attributes:
        _url (str): The URL to the OpenAPI specification file.
        _remove_prefix (str): The prefix to remove from the endpoint paths when
            generating function names.
        _functions (dict): A dictionary of all the generated endpoint functions.
    """

    _url: str | None = None
    _remove_prefix: str | None = None
    _functions: dict = {}

    def __init__(self, url: str, *, remove_prefix: str | None = None):
        self._url = url
        self._remove_prefix = remove_prefix
        self._functions = generate_tools(url, remove_prefix)

    def get_function_tools(self) -> dict:
        """
        Return a dictionary of all the generated endpoint functions.

        The returned dictionary has the function names as keys and the
        dictionaries returned by the generator as values. Each dictionary
        contains the function itself, the Pydantic model for parameter validation,
        and a description string.

        The purpose of this function is to allow the caller to inspect or
        modify the generated functions.

        Returns:
            dict: A dictionary of all the generated endpoint functions.
        """
        return self._functions
    
    def get_openai_tools(self) -> list[FunctionTool]:
        """
        Generate a list of OpenAI FunctionTool objects from the endpoints.

        Each endpoint is converted into a FunctionTool, which is a callable
        object with a name, description, JSON schema for parameters, and a function
        that will be called when the tool is invoked.

        The generated FunctionTools are returned as a list.
        """
        tools: list[FunctionTool] = []
 
        for func_name, item in self._functions.items():
            # Create a factory function to properly capture the current value of 'item'
            def create_run_function(current_item):
                async def run_function(ctx: RunContextWrapper[Any], args: str):
                    parsed = current_item["model"].model_validate_json(args)
                    # Convert Pydantic model to dictionary before passing to function
                    parsed_dict = parsed.model_dump()
                    return current_item["func"](**parsed_dict)
                return run_function

            # Get the JSON schema and ensure additionalProperties is set to false
            # Also remove default values which are not allowed by OpenAI
            # And ensure all properties are marked as required
            schema = item["model"].model_json_schema()
            if "properties" in schema:
                schema["additionalProperties"] = False
                
                # Remove default values from properties
                for prop_name, prop_schema in schema["properties"].items():
                    if "default" in prop_schema:
                        del prop_schema["default"]
                
                # Ensure all properties are marked as required
                schema["required"] = list(schema["properties"].keys())
            
            tools.append(FunctionTool(
                name=func_name,
                description=item["description"],
                params_json_schema=schema,
                on_invoke_tool=create_run_function(item),
            ))

        return tools