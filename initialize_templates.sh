#!/bin/bash

set -euo pipefail

script_dir=".init_wizard/"
container_template_sources="/ws"
container_template_target_dir="/source"
host_sources="."

pip_requirements="questionary==2.1.0 jinja2==3.0.0"

if [ ! -d "${script_dir}" ]; then
  echo -e "\033[31mThe initialization wizard has already been run. Exiting...\033[0m"
  exit 1
fi
if [ -d "${host_sources}/source" ]; then
  echo -e "\033[31mHost source directory \"${host_sources}/source\" exists, but the initialization wizard has still not been marked as run. This may indicate a previous failure. Re-running the initialization wizard might not fix the issue.\033[0m"
fi

docker run --rm -it \
    -e IN_DOCKER=1 \
    -e UID="$(id -u)" \
    -e GID="$(id -g)" \
    -e TEMPLATE_SOURCES="${container_template_sources}" \
    -e TEMPLATE_TARGET_DIR="${container_template_target_dir}" \
    -v "${script_dir}:${container_template_sources}" \
    -v "${host_sources}:${container_template_target_dir}" \
    python:3.12-slim \
    bash -c "pip install ${pip_requirements} >> /dev/null 2>&1 && python3 /${container_template_sources}/initialize_package.py"

if [ ! -d "${script_dir}/templates" ]; then
  rm -rf "${script_dir}" # all went well, self-delete wizard
fi
