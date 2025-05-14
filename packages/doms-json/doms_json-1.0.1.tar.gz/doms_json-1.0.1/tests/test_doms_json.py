from doms_json import *
from typing import Literal


class MyObject:
    def __init__(self, my_variable: str, my_second_variable: int) -> None:
        self.my_variable: str = my_variable
        self.my_second_variable: int = my_second_variable

class MyObjectDocstrings:
    def __init__(self, my_variable: str) -> None:
        """
        :param my_variable: A simple string variable
        """
        self.my_variable: str = my_variable

def my_function(int_variable: int | None, str_variable: str = "This is a string"):...

class MyClass:
    names: list[str]

def get_weather(date: str, city: str, state: str) -> str:
    return f"Date: {date}, City: {city}, State: {state}"

class Location:
    def __init__(self, city: str, state: str) -> None:
        self.city: str = city
        self.state: str = state

def get_weather_object(date: str, location: Location) -> str:
    return f"Date: {date}, City: {location.city}, State: {location.state}"

def get_weather_list_object(values: list[Location | int]) -> str:
    string: str = ""
    for value in values:
        if type(value) == Location:
            string += f"{value.city}-{value.state}, "
        else:
            string += f"{value}"
    return string

def get_weather_list_or_not(date: str, locations: Location | list[Location | int]) -> str:
    if type(locations) == Location:
        return get_weather_object(date, locations)
    return get_weather_list_object(locations)

def multi_object(location: Location, my_object: MyObject, either: Location | MyObject) -> str:
    return {
        "location": vars(location),
        "my_object": vars(my_object),
        "either": vars(either)
    }

def literal_function(literal_string: Literal["Value One", "Value Two", "Value Three"], literal_int: Literal[0, 1, 2]) -> str:
    return f"{literal_string} - {literal_int}"

def test_doms_json():
    # Create JSON schema with no types
    response = create_json_schema(["my_variable", "my_second_variable"], additional_properties=True)
    assert response == {
        "type": "object",
        "properties": {
            "my_variable": { },
            "my_second_variable": { }
        },
        "additionalProperties": True
    }
    # Create JSON schema with types
    types = {
        "my_variable": str,
        "my_second_variable": int
    }
    response = create_json_schema(["my_variable", "my_second_variable"], types)
    assert response == {
        "type": "object",
        "properties": {
            "my_variable": {
                "type": "string"
            },
            "my_second_variable": {
                "type": "integer"
            }
        },
        "additionalProperties": False
    }
    # Create JSON schema with defaults
    defaults = {
        "my_variable": "Hello world!"
    }
    response = create_json_schema(["my_variable", "my_second_variable"], defaults=defaults)
    assert response == {
        "type": "object",
        "properties": {
            "my_variable": {
                "default": "Hello world!"
            },
            "my_second_variable": { }
        },
        "additionalProperties": False
    }
    # Create JSON schema with defaults and types
    response = create_json_schema(["my_variable", "my_second_variable"], types, defaults)
    assert response == {
        "type": "object",
        "properties": {
            "my_variable": {
                "default": "Hello world!",
                "type": "string"
            },
            "my_second_variable": {
                "type": "integer"
            }
        },
        "additionalProperties": False
    }
    # Create JSON schema with descriptions
    descriptions = {
        "my_second_variable": "The number of lines of code"
    }
    response = create_json_schema(["my_variable", "my_second_variable"], descriptions=descriptions)
    assert response == {
        "type": "object",
        "properties": {
            "my_variable": { },
            "my_second_variable": {
                "description": "The number of lines of code"
            }
        },
        "additionalProperties": False
    }
    # Create JSON schema with descriptions, defaults, and types
    response = create_json_schema(["my_variable", "my_second_variable"], types, defaults, descriptions)
    assert response == {
        "type": "object",
        "properties": {
            "my_variable": {
                "default": "Hello world!",
                "type": "string"
            },
            "my_second_variable": {
                "type": "integer",
                "description": "The number of lines of code"
            }
        },
        "additionalProperties": False
    }
    # Create JSON schema with requirements
    response = create_json_schema(["my_variable", "my_second_variable"], required=["my_variable"])
    assert response == {
        "type": "object",
        "properties": {
            "my_variable": { },
            "my_second_variable": { }
        },
        "required": ["my_variable"],
        "additionalProperties": False
    }
    # Create JSON schema with required, descriptions, defaults, and types
    response = create_json_schema(["my_variable", "my_second_variable"], types, defaults, descriptions, ["my_variable"])
    assert response == {
        "type": "object",
        "properties": {
            "my_variable": {
                "default": "Hello world!",
                "type": "string"
            },
            "my_second_variable": {
                "type": "integer",
                "description": "The number of lines of code"
            }
        },
        "required": ["my_variable"],
        "additionalProperties": False
    }
    # Create JSON schema with a title
    response = create_json_schema(["my_variable", "my_second_variable"], title="MySchema")
    assert response == {
        "type": "object",
        "title": "MySchema",
        "properties": {
            "my_variable": { },
            "my_second_variable": { }
        },
        "additionalProperties": False
    }
    # Create JSON schema with a title, required, descriptions, defaults, and types
    response = create_json_schema(["my_variable", "my_second_variable"], types, defaults, descriptions, ["my_variable"], "MySchema")
    assert response == {
        "type": "object",
        "title": "MySchema",
        "properties": {
            "my_variable": {
                "default": "Hello world!",
                "type": "string"
            },
            "my_second_variable": {
                "type": "integer",
                "description": "The number of lines of code"
            }
        },
        "required": ["my_variable"],
        "additionalProperties": False
    }
    # Create JSON schema from object
    response = generate_json_schema(MyObject)
    assert response == {
        "type": "object",
        "title": "MyObject",
        "properties": {
            "my_variable": {
                "type": "string"
            },
            "my_second_variable": {
                "type": "integer"
            }
        },
        "required": ["my_variable", "my_second_variable"],
        "additionalProperties": False
    }
    # Create JSON schema from function
    response = generate_json_schema(my_function)
    assert response == {
        "type": "object",
        "title": "my_function",
        "properties": {
            "int_variable": {
                "type": "integer"
            },
            "str_variable": {
                "type": "string",
                "default": "This is a string"
            }
        },
        "required": ["str_variable"],
        "additionalProperties": False
    }
    # Create JSON schema from class
    response = generate_json_schema(MyClass)
    assert response == {
        "type": "object",
        "title": "MyClass",
        "properties": {
            "names": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["names"],
        "additionalProperties": False
    }
    # Create JSON schema from object with Docstrings
    response = generate_json_schema(MyObjectDocstrings)
    assert response == {
        "type": "object",
        "title": "MyObjectDocstrings",
        "properties": {
            "my_variable": {
                "type": "string",
                "description": "A simple string variable"
            }
        },
        "required": ["my_variable"],
        "additionalProperties": False
    }
    # Manually describe a JSON schema
    schema = {
        "type": "object",
        "properties": {
            "my_object": {
                "type": "object",
                "properties": {
                    "my_string": {
                        "type": "string"
                    }
                }
            },
            "my_number": {
                "type": "integer"
            }
        },
        "additionalProperties": False
    }
    descriptions = {
        "my_object": "An object",
        "my_number": "An integer"
    }
    response = describe_json_schema(schema, descriptions)
    assert response == {
        "type": "object",
        "properties": {
            "my_object": {
                "type": "object",
                "description": "An object",
                "properties": {
                    "my_string": {
                        "type": "string"
                    }
                }
            },
            "my_number": {
                "type": "integer",
                "description": "An integer"
            }
        },
        "additionalProperties": False
    }
    descriptions = {
        "my_object": {
            "my_string": "A string"
        },
        "my_number": "An integer"
    }
    response = describe_json_schema(schema, descriptions)
    assert response == {
        "type": "object",
        "properties": {
            "my_object": {
                "type": "object",
                "properties": {
                    "my_string": {
                        "type": "string",
                        "description": "A string"
                    }
                }
            },
            "my_number": {
                "type": "integer",
                "description": "An integer"
            }
        },
        "additionalProperties": False
    }
    descriptions = {
        "my_object": {
            "properties": {
                "my_string": "A string"
            },
            "description": "An object"
        },
        "my_number": "An integer"
    }
    response = describe_json_schema(schema, descriptions)
    assert response == {
        "type": "object",
        "properties": {
            "my_object": {
                "type": "object",
                "description": "An object",
                "properties": {
                    "my_string": {
                        "type": "string",
                        "description": "A string"
                    }
                }
            },
            "my_number": {
                "type": "integer",
                "description": "An integer"
            }
        },
        "additionalProperties": False
    }
    # Convert a type to a JSON Schema Type
    response = to_json_schema_type(str)
    assert vars(response) == vars(JSONSchemaType({"type": "string"}, True))
    # Convert a type to a direct JSON schema type
    response = to_direct_json_schema_type(str)
    assert response == "string"
    # Call a function with JSON call
    llm_response = {
        "date": "2025-01-01",
        "city": "Dallas",
        "state": "Texas"
    }
    response = json_call(get_weather, llm_response)
    assert response == "Date: 2025-01-01, City: Dallas, State: Texas"
    # Call a function that has object inputs with JSON call
    llm_response = {
        "date": "2025-01-01",
        "location": {
            "city": "Dallas",
            "state": "Texas"
        }
    }
    response = json_call(get_weather_object, llm_response)
    assert response == "Date: 2025-01-01, City: Dallas, State: Texas"
    # Call a function that has an object as part of another typep
    llm_response = {
        "values": [
            {
                "city": "Dallas",
                "state": "Texas"
            },
            {
                "city": "New York",
                "state": "New York"
            },
            1
        ]
    }
    response = json_call(get_weather_list_object, llm_response)
    assert response == "Dallas-Texas, New York-New York, 1"
    # Call a function that can have a list or not a list
    llm_response = {
        "date": "2025-01-01",
        "locations": [
            {
                "city": "Dallas",
                "state": "Texas"
            },
            {
                "city": "New York",
                "state": "New York"
            }
        ]
    }
    response = json_call(get_weather_list_or_not, llm_response)
    assert response == "Dallas-Texas, New York-New York, "
    # Call a function that has multiple objects, some Unioned
    llm_response = {
        "location": {
            "city": "Dallas",
            "state": "Texas"
        },
        "my_object": {
            "my_variable": "Test",
            "my_second_variable": 1
        },
        "either": {
            "city": "New York",
            "state": "New York"
        }
    }
    response = json_call(multi_object, llm_response)
    assert response == llm_response
    # Test that literals convert to string enums
    schema = {
        "type": "object",
        "title": "literal_function",
        "properties": {
            "literal_string": {
                "type": "string",
                "enum": ["Value One", "Value Two", "Value Three"]
            },
            "literal_int": {
                "type": "integer",
                "enum": [0, 1, 2]
            }
        },
        "required": ["literal_string", "literal_int"],
        "additionalProperties": False
    }
    assert schema == generate_json_schema(literal_function)
    # Test that literals process through json_calls and molding properly
    llm_response = {
        "literal_string": "Value One",
        "literal_int": 2
    }
    response = json_call(literal_function, llm_response)
    assert response == "Value One - 2"
    llm_response = {
        "literal_string": "Value Four",
        "literal_int": 2
    }
    try:
        json_call(literal_function, llm_response)
    except Exception as e:
        assert type(e) == TypeMismatch
        assert f"{e}" == f"Value \033[31mValue Four\033[37m could not be molded into any of the expected literal values: \033[31m('Value One', 'Value Two', 'Value Three')\033[37m"