import os
from importlib.util import find_spec
from typing import Optional

from jinja2 import Template

import fastapi_gen
from fastapi_gen.exceptions import CommandError


class CommandUtility:
    def __init__(self, project_name: str, target: Optional[str]):
        self.name = project_name
        self.target = target
        self.rewrite_template_suffixes = ((".jinja2", ".py"),)

    def validate_name(self):
        if not self.name.isidentifier():
            raise CommandError(
                f"'{self.name}' is not a valid a Project. Please make sure the project name is a valid identifier."
            )

        if find_spec(self.name) is not None:
            raise CommandError(
                f"'{self.name}' conflicts with the name of an existing Python "
                "module and cannot be used as a Project name. Please try "
                "another name."
            )

    def handle_template(self, top_dir: str):
        base_name = "project_name"
        base_subdir = "project_template"
        app_base_name = "app_name"
        app_name = "app"
        next_app_name = "main"
        flag = 0
        is_main = str(self.name) == next_app_name
        template_dir = os.path.join(fastapi_gen.__path__[0], "core", base_subdir)
        prefix_length = len(template_dir) + 1
        context = {base_name: self.name}
        for root, _, files in os.walk(template_dir):
            path_rest = root[prefix_length:]
            relative_dir = path_rest.replace(base_name, self.name)
            if relative_dir:
                target_dir = os.path.join(top_dir, relative_dir)
                os.makedirs(target_dir, exist_ok=True)

            for filename in files:
                if filename.endswith((".pyo", ".pyc", ".py.class")):
                    # Ignore some files as they cause various breakages.
                    continue
                old_path = os.path.join(root, filename)
                if is_main and flag == 0:
                    replaced_file = filename.replace(app_base_name, app_name)
                    flag = 1
                else:
                    replaced_file = filename.replace(app_base_name, next_app_name)
                new_path = os.path.join(top_dir, relative_dir, replaced_file)
                for old_suffix, new_suffix in self.rewrite_template_suffixes:
                    if new_path.endswith(old_suffix):
                        new_path = new_path.removesuffix(old_suffix) + new_suffix
                        break

                if os.path.exists(new_path):
                    raise CommandError(
                        f"{new_path} already exists. Overlaying a Project into an existing "
                        "directory won't replace conflicting files."
                    )

                with open(old_path, encoding="utf-8") as template_file:
                    content = template_file.read()
                template = Template(content)
                content = template.render(**context)
                with open(new_path, "w", encoding="utf-8") as new_file:
                    new_file.write(content)

    def handle(self):
        target = self.target
        if target is None:
            top_dir = os.path.join(os.getcwd(), self.name)
            try:
                os.makedirs(top_dir)
            except FileExistsError:
                raise CommandError(f"'{top_dir}' already exists")
        else:
            top_dir = os.path.abspath(os.path.expanduser(target))
            if not os.path.exists(top_dir):
                raise CommandError(
                    f"Destination directory '{top_dir}' does not "
                    "exist, please create it first."
                )
        self.handle_template(top_dir)

    def execute(self):
        self.validate_name()
        self.handle()
