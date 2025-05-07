class RenderedTemplate:
    """
    A wrapper class for a rendered Jinja2 template.
    Provides utility methods to convert the rendered text to JSON or YAML formats.
    """

    def __init__(self, rendered_text: str):
        """
        Initializes the RenderedTemplate with the given rendered text.

        Args:
            rendered_text (str): The output string from rendering a Jinja2 template.
        """
        self.text = rendered_text

    def __str__(self):
        """
        Returns the raw rendered template as a string.

        Returns:
            str: The rendered template text.
        """
        return self.text

    def json(self):
        """
        Parses the rendered YAML text into a Python dictionary.

        Returns:
            dict: Parsed representation of the rendered YAML.
        """
        from yaml import safe_load
        return safe_load(self.text)

    def yaml(self):
        """
        Converts the parsed JSON (dictionary) back into a YAML-formatted string.

        Returns:
            str: YAML representation of the rendered template.
        """
        from yaml import dump
        return dump(self.json(), sort_keys=False, allow_unicode=True)


class LoadTemplate:
    """
    Loads and renders a Jinja2 template from the local templates directory.
    """

    def __init__(self, templateName: str):
        """
        Initializes the template loader and retrieves the specified template.

        Args:
            templateName (str): The filename of the template to load (e.g., 'ip.yml.j2').
        """
        self.__retrieveTemplate__(templateName)

    def __retrieveTemplate__(self, templateName: str) -> None:
        """
        Locates and loads the Jinja2 template from the 'templates' directory.

        Args:
            templateName (str): The filename of the Jinja2 template to load.
        """
        from os.path import (
            abspath, 
            dirname, 
            join
        )
        from jinja2 import (
            Environment,
            FileSystemLoader
        )

        base_dir = dirname(abspath(__file__))
        template_dir = join(base_dir, 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        self.template = env.get_template(templateName)

    def render(self, context: dict):
        """
        Renders the loaded template with the provided context.

        Args:
            context (dict): Dictionary of values to inject into the template.

        Returns:
            RenderedTemplate: An object containing the rendered result.
        """
        return RenderedTemplate(self.template.render(context))