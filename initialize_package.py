#!/usr/bin/env python3
import os
import re
import subprocess
from pathlib import Path

from initialization_wizard_utils.filesystem import (
    rm_files,
    sed_in_place,
    sed_remove_line_matching,
    sed_remove_range,
    replace_text_in_file,
    traverse_and_rename,
)
from initialization_wizard_utils.globals import (
    TEMPLATE_SOURCES,
    OG_CONTROLLER_PACKAGE,
    OG_CONTROLLER_NAME,
    OG_COMPONENT_PACKAGE,
    OG_COLLECTION_NAME,
    PYTHON_COMPONENT_FILES,
    CPP_COMPONENT_FILES,
)

PIP_REQUIREMENTS = {
    "questionary": "==2.1.0",
}


def is_inside_docker() -> bool:
    return os.environ.get("IN_DOCKER") == "1"


def outside_docker_behavior():
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent
    docker_cmd = [
        "docker",
        "run",
        "--rm",
        "-it",
        "-e",
        "IN_DOCKER=1",
        "-v",
        f"{script_dir}:/{TEMPLATE_SOURCES}",
        "python:3.12-slim",
        "python",
        f"/{TEMPLATE_SOURCES}/{script_path.name}",
    ]
    subprocess.run(docker_cmd, check=True)


def inside_docker_behavior():
    install_requirements()
    run_wizard()


def install_requirements():
    path = "/tmp/requirements.txt"
    with open(path, "w", encoding="utf-8") as f:
        for pkg, version in PIP_REQUIREMENTS.items():
            line = f"{pkg}{version}\n"
            f.write(line)
    subprocess.run(["pip", "install", "-r", path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def run_wizard():
    from initialization_wizard_utils.questions import (
        AVAILABLE_TEMPLATES_Q,
        CONTROLLER_PACKAGE_Q,
        CONTROLLER_NAME_Q,
        HARDWARE_IF_Q,
        COMPONENT_PACKAGE_Q,
        TEMPLATES_TO_INCLUDE_Q,
        VSCODE_DEFAULTS_Q,
        COLLECTION_NAME_Q,
        CONFIRMATION_Q,
    )

    if (
        not Path(f"{TEMPLATE_SOURCES}/source/{OG_CONTROLLER_PACKAGE}").exists()
        or not Path(f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}").exists()
    ):
        print("Seems like the wizard has already been run before, exiting.")
        return

    print(
        "This package initialization wizard will help you set up your development environment,"
        " please carefully follow the prompts."
    )

    # template selection
    packages = AVAILABLE_TEMPLATES_Q.ask()

    configuration = {}

    if "Controllers" in packages:
        controller_configuration = {}
        controller_configuration["Package name"] = CONTROLLER_PACKAGE_Q.ask()
        controller_configuration["Controller name"] = CONTROLLER_NAME_Q.ask()
        controller_configuration["Hardware interface"] = HARDWARE_IF_Q.ask()
        configuration["controller"] = controller_configuration
        print("-- Controller configuration complete\n")

    if "Components" in packages:
        component_configuration = {}
        component_configuration["Package name"] = COMPONENT_PACKAGE_Q.ask()
        component_configuration["Template components to include"] = TEMPLATES_TO_INCLUDE_Q.ask()
        configuration["component"] = component_configuration
        print("-- Component configuration complete\n")

    if ["controller", "component"] == list(configuration.keys()):
        if configuration["controller"]["Package name"] == configuration["component"]["Package name"]:
            print("Controller and component package names must be different.")
            return
        configuration["VSCode default package"] = VSCODE_DEFAULTS_Q(configuration).ask()
        configuration["Collection name"] = COLLECTION_NAME_Q.ask()
        print("-- VSCode and collection configuration complete\n")

    print_configuration(configuration)
    if CONFIRMATION_Q.ask():
        update_vscode_defaults(configuration)
        perform_initialization(configuration)


def print_configuration(configuration):
    print("\nConfiguration:\n")
    for key, value in configuration.items():
        if isinstance(value, dict):
            print(f"\t{key.capitalize()}:")
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, list):
                    for list_item in sub_value:
                        print(f"\t\t- {sub_key}: {list_item}")
                else:
                    print(f"\t\t{sub_key}: {sub_value}")
        else:
            v = value
            if value in OG_COMPONENT_PACKAGE:
                v = configuration["component"]["Package name"]
            elif value in OG_CONTROLLER_PACKAGE:
                v = configuration["controller"]["Package name"]
            print(f"\t{key.capitalize()}: {v}")


def perform_initialization(configuration: dict):
    for key, data in configuration.items():
        match key.lower():
            case "controller":
                initialize_controllers(data)
            case "component":
                initialize_components(data)

def update_vscode_defaults(configuration: dict):
    if "Collection name" in configuration.keys():
        collection_name = configuration["Collection name"]
        sed_in_place(
            f"{TEMPLATE_SOURCES}/aica-package.toml",
            f"{OG_COLLECTION_NAME}",
            f"{collection_name.replace('_', '-')}",
        )
        sed_in_place(
            f"{TEMPLATE_SOURCES}/aica-package.toml",
            f"{OG_COLLECTION_NAME.replace('-', '_')}",
            f"{collection_name}",
        )
    else:
        if "controller" in configuration:
            rm_files([f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}"])
            configuration["VSCode default package"] = OG_CONTROLLER_PACKAGE
            sed_remove_range(
                filepath=f"{TEMPLATE_SOURCES}/aica-package.toml",
                start_pattern=r"\[build.packages.template-component-package\]",
                end_pattern="# numpy = \"1.0.0\"",
            )
        elif "component" in configuration:
            rm_files([f"{TEMPLATE_SOURCES}/source/{OG_CONTROLLER_PACKAGE}"])
            configuration["VSCode default package"] = OG_COMPONENT_PACKAGE
            sed_remove_range(
                filepath=f"{TEMPLATE_SOURCES}/aica-package.toml",
                start_pattern=r"\[build.packages.template-controller-package\]",
                end_pattern="# libyaml-cpp-dev = \"*\"",
            )
        sed_in_place(
            f"{TEMPLATE_SOURCES}/aica-package.toml",
            "[metadata.collection]",
            "# [metadata.collection]",
        )
        sed_in_place(
            f"{TEMPLATE_SOURCES}/aica-package.toml",
            "name = \"template-custom-collection\"",
            "# name = \"template-custom-collection\"",
        )
        sed_in_place(
            f"{TEMPLATE_SOURCES}/aica-package.toml",
            "ros-name = \"template_custom_collection\"",
            "# ros-name = \"template_custom_collection\"",
        )

    for file in [
        f"{TEMPLATE_SOURCES}/.devcontainer/devcontainer.json",
        f"{TEMPLATE_SOURCES}/.vscode/settings.json",
    ]:
        replace_text_in_file(
            file,
            OG_COMPONENT_PACKAGE,
            configuration["VSCode default package"],
        )

def initialize_controllers(configuration: dict):
    from initialization_wizard_utils.questions import camel_to_snake

    new_controller_snake_case = camel_to_snake(configuration["Controller name"])
    old_controller_snake_case = camel_to_snake(OG_CONTROLLER_NAME)

    file_list = [f for f in Path(f"{TEMPLATE_SOURCES}/source/{OG_CONTROLLER_PACKAGE}").glob("**/*") if f.is_file()]
    for file in file_list + [
        f"{TEMPLATE_SOURCES}/.github/workflows/build-test.yml",
        f"{TEMPLATE_SOURCES}/aica-package.toml",
        f"{TEMPLATE_SOURCES}/.devcontainer/devcontainer.json",
        f"{TEMPLATE_SOURCES}/.vscode/settings.json",
    ]:
        if os.path.isfile(file):
            replace_text_in_file(
                file,
                OG_CONTROLLER_PACKAGE,
                configuration["Package name"],
            )
            replace_text_in_file(
                file,
                OG_CONTROLLER_NAME,
                configuration["Controller name"],
            )
            replace_text_in_file(
                file,
                old_controller_snake_case,
                new_controller_snake_case,
            )
            sed_in_place(
                file,
                "HW_IF_POSITION",
                "HW_IF_" + configuration["Hardware interface"].upper(),
            )
            sed_in_place(
                file,
                '"control_type": "position"',
                '"control_type": "' + configuration["Hardware interface"].lower() + '"',
            )

    traverse_and_rename(
        source_path=Path(f"{TEMPLATE_SOURCES}/source/"),
        old_name=OG_CONTROLLER_PACKAGE,
        new_name=configuration["Package name"],
    )
    traverse_and_rename(
        source_path=Path(f"{TEMPLATE_SOURCES}/source/"),
        old_name=old_controller_snake_case,
        new_name=new_controller_snake_case,
    )


def initialize_components(configuration: dict):
    setup_cfg = f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/setup.cfg"
    cmakelists = f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/CMakeLists.txt"
    selected = configuration["Template components to include"]

    # Python components
    if not ("Python component" in selected or "Python Lifecycle component" in selected):
        rm_files(PYTHON_COMPONENT_FILES["common"])
        sed_in_place(cmakelists, "ament_python_install_package()", "")
    else:
        if "Python component" not in selected:
            rm_files(PYTHON_COMPONENT_FILES["component"])
            sed_remove_line_matching(rf"{re.escape(OG_COMPONENT_PACKAGE)}::PyComponent", setup_cfg)

        if "Python Lifecycle component" not in selected:
            rm_files(PYTHON_COMPONENT_FILES["lifecycle"])
            sed_remove_line_matching(rf"{re.escape(OG_COMPONENT_PACKAGE)}::PyLifecycleComponent", setup_cfg)

    # C++ components
    if not ("C++ component" in selected or "C++ Lifecycle component" in selected):
        rm_files(CPP_COMPONENT_FILES["common"])
        sed_remove_range(
            filepath=cmakelists,
            start_pattern=r"### Register C\+\+ Components ###",
            end_pattern=r"RUNTIME DESTINATION bin\)",
        )
    else:
        if "C++ component" not in selected:
            rm_files(CPP_COMPONENT_FILES["component"])
            sed_remove_range(
                filepath=cmakelists,
                start_pattern=r"Register CPPComponent",
                end_pattern=r"COMPONENTS cpp_component\)",
            )

        if "C++ Lifecycle component" not in selected:
            rm_files(CPP_COMPONENT_FILES["lifecycle"])
            sed_remove_range(
                filepath=cmakelists,
                start_pattern=r"Register CPPLifecycleComponent",
                end_pattern=r"COMPONENTS cpp_lifecycle_component\)",
            )

    new_package_name = configuration["Package name"]
    for file in [
        f"{TEMPLATE_SOURCES}/.github/workflows/build-test.yml",
        f"{TEMPLATE_SOURCES}/aica-package.toml",
        f"{TEMPLATE_SOURCES}/.devcontainer/devcontainer.json",
        f"{TEMPLATE_SOURCES}/.vscode/settings.json",
    ]:
        replace_text_in_file(file, OG_COMPONENT_PACKAGE, new_package_name)

    traverse_and_rename(
        source_path=Path(f"{TEMPLATE_SOURCES}/source/"),
        old_name=OG_COMPONENT_PACKAGE,
        new_name=new_package_name,
    )


if __name__ == "__main__":
    if is_inside_docker():
        inside_docker_behavior()
    else:
        outside_docker_behavior()
