try:
    import questionary # type: ignore
    from questionary import Choice  # type: ignore
except ImportError:
    raise ImportError("Please install the 'questionary' package to use this script.")

import re
from initialization_wizard_utils.globals import (
    OG_CONTROLLER_PACKAGE,
    OG_COMPONENT_PACKAGE,
    NAME_BLACKLIST,
)

def is_snake_case(value: str) -> bool:
    pattern = r"^[a-z]+(?:_[a-z0-9]+)*$"
    if re.match(pattern, value):
        return True
    return False


def is_camel_case(value: str) -> bool:
    pattern = r"^[a-zA-Z]+(?:[A-Z][a-z0-9]*)*$"
    if re.match(pattern, value):
        return True
    return False


def camel_to_snake(name: str) -> str:
    s1 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    s2 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s1)
    return s2.lower()


def is_valid_package_name(value: str) -> bool:
    return value not in NAME_BLACKLIST


CONFIRMATION_Q = questionary.confirm("Are you happy with this configuration?", default=True)

COLLECTION_NAME_Q = questionary.text(
            "Choose a ROS collection name (snake_case):",
            default="",
            validate=lambda text: text.strip() != "" and is_snake_case(text) and is_valid_package_name(text),
        )

# Available templates
AVAILABLE_TEMPLATES_Q = questionary.checkbox(
        "Which packages would you like to include in your development environment?",
        choices=[
            {"name": "Components", "checked": True},
            {"name": "Controllers", "checked": True},
        ],
        validate=lambda choices: len(choices) > 0,
    )

# Controllers
CONTROLLER_PACKAGE_Q = questionary.text(
            "Enter the new controller package name (snake_case):",
            default="",
            validate=lambda text: text.strip() != "" and is_snake_case(text) and is_valid_package_name(text),
        )

CONTROLLER_NAME_Q = questionary.text(
            "Enter the desired controller name (CamelCase):",
            default="",
            validate=lambda text: text.strip() != "" and is_camel_case(text),
        )

HARDWARE_IF_Q = questionary.select(
            "Select the type of hardware interface you want to use:",
            choices=["Position", "Velocity", "Effort"],
        )

# Components
COMPONENT_PACKAGE_Q = questionary.text(
            "Enter the new component package name (snake_case):",
            default="",
            validate=lambda text: text.strip() != "" and is_snake_case(text) and is_valid_package_name(text),
        )

TEMPLATES_TO_INCLUDE_Q = questionary.checkbox(
            "Select the types of components you want to include:",
            choices=[
                Choice(title="Python Lifecycle component", checked=True),
                Choice(title="Python component", checked=True),
                Choice(title="C++ Lifecycle component", checked=True),
                Choice(title="C++ component", checked=True),
            ],
            validate=lambda choices: len(choices) > 0,
        )

# VSCode Defaults
def VSCODE_DEFAULTS_Q(configuration: dict):
    return questionary.select(
            "Which package would you like to use for VSCode and devcontainer settings?",
            choices=[
                Choice(title=configuration["component"]["Package name"], value=OG_COMPONENT_PACKAGE),
                Choice(title=configuration["controller"]["Package name"], value=OG_CONTROLLER_PACKAGE),
            ],
        )