from typing import Optional, List

from jinja2 import Environment, FileSystemLoader, PackageLoader, TemplateNotFound


class FHStylesLoader:
    def __init__(self, extra_resources: Optional[List] = None):
        if extra_resources is None:
            extra_resources = []
        elif isinstance(extra_resources, str):
            extra_resources = [extra_resources]

        self.extra_resources = extra_resources

        self.env = Environment(
            loader=PackageLoader("floods_html", "styles"),
            autoescape=True,
        )

        self.extra_envs = [
            Environment(loader=FileSystemLoader(extrapath), autoescape=True) for extrapath in self.extra_resources
        ]

    def get_resource(self, name: str):
        """
        Get *first* match from the package resources and extra paths, in order of initialisation.
        """
        try:
            return self.env.get_template(name)
        except TemplateNotFound:
            for extra_env in self.extra_envs:
                try:
                    return extra_env.get_template(name)
                except TemplateNotFound:
                    continue
            raise TemplateNotFound("Template not found in any loader")
