NAME_BLACKLIST = ["controller", "component", "template_component_package", "template_controller_package", "src", "test"]

OG_CONTROLLER_PACKAGE = "template_controller_package"
OG_CONTROLLER_NAME = "TemplateController"
OG_COMPONENT_PACKAGE = "template_component_package"
OG_COLLECTION_NAME = "template-custom-collection"
TEMPLATE_SOURCES = "/template_sources"

PYTHON_COMPONENT_FILES = {
    "common": [
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/requirements.txt",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/setup.cfg",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/{OG_COMPONENT_PACKAGE}",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/test/python_tests",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/component_descriptions/{OG_COMPONENT_PACKAGE}_py_component.json",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/component_descriptions/{OG_COMPONENT_PACKAGE}_py_lifecycle_component.json",
    ],
    "component": [
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/{OG_COMPONENT_PACKAGE}/py_component.py",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/test/python_tests/test_py_component.py",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/component_descriptions/{OG_COMPONENT_PACKAGE}_py_component.json",
    ],
    "lifecycle": [
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/{OG_COMPONENT_PACKAGE}/py_lifecycle_component.py",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/test/python_tests/test_py_lifecycle_component.py",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/component_descriptions/{OG_COMPONENT_PACKAGE}_py_lifecycle_component.json",
    ],
}

CPP_COMPONENT_FILES = {
    "common": [
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/include",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/src",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/test/cpp_tests",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/test/test_cpp_components.cpp",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/component_descriptions/{OG_COMPONENT_PACKAGE}_cpp_component.json",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/component_descriptions/{OG_COMPONENT_PACKAGE}_cpp_lifecycle_component.json",
    ],
    "component": [
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/src/CPPComponent.cpp",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/test/cpp_tests/test_cpp_component.cpp",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/include/{OG_COMPONENT_PACKAGE}/CPPComponent.hpp",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/component_descriptions/{OG_COMPONENT_PACKAGE}_cpp_component.json",
    ],
    "lifecycle": [
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/src/CPPLifecycleComponent.cpp",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/test/cpp_tests/test_cpp_lifecycle_component.cpp",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/include/{OG_COMPONENT_PACKAGE}/CPPLifecycleComponent.hpp",
        f"{TEMPLATE_SOURCES}/source/{OG_COMPONENT_PACKAGE}/component_descriptions/{OG_COMPONENT_PACKAGE}_cpp_lifecycle_component.json",
    ],
}
