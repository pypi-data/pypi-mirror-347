import jinja2
import pytest
import importlib.resources as resources
import pathlib

from floods_html.styles import FHStylesLoader


def test_styles_loader_creation():
    """
    basic creation test
    """

    # Create a template loader
    template_loader = FHStylesLoader()

    # Check that the styles loader is created correctly
    assert template_loader is not None

    # Check that the styles loader has the correct attributes
    assert hasattr(template_loader, "env")

    assert isinstance(template_loader.env, jinja2.environment.Environment)

    templates_path = resources.files("floods_html.styles")
    one_tmplt = (f for f in pathlib.Path(templates_path).glob("*") if not (f.name.endswith(".py") or f.is_dir()))
    template_loader.get_resource(next(one_tmplt).name)

    with pytest.raises(jinja2.TemplateNotFound):
        template_loader.get_resource("non_existent_template.css")


def test_styles_loader_with_extra_templates(tmp_path):
    """
    Test the styles loader with dummy extra templates
    """

    # Create a template loader with an extra template
    extra_template_path = tmp_path.joinpath("flood-html-test-templates")
    extra_template_path.mkdir(parents=True, exist_ok=True)
    with open(extra_template_path.joinpath("test.html.jinja"), "w") as f:
        f.write("<html><head></head><body></body></html>")

    single_template_loader = FHStylesLoader(extra_resources=extra_template_path.as_posix())

    # Check that the styles loader is created correctly
    assert single_template_loader is not None

    # Check that the styles loader has the correct attributes
    assert hasattr(single_template_loader, "env")

    assert isinstance(single_template_loader.env, jinja2.environment.Environment)

    templates_path = resources.files("floods_html.styles")
    one_tmplt = (f for f in pathlib.Path(templates_path).glob("*") if not (f.name.endswith(".py") or f.is_dir()))
    single_template_loader.get_resource(next(one_tmplt).name)

    single_template_loader.get_resource("test.html.jinja")

    with pytest.raises(jinja2.TemplateNotFound):
        single_template_loader.get_resource("non_existent_template.css")


def test_multiple_extra_loaders(tmp_path):
    """
    Test the styles loader with multiple extra templates
    """

    extra_template_path = tmp_path.joinpath("flood-html-test-templates")
    extra_template_path.mkdir(parents=True, exist_ok=True)
    with open(extra_template_path.joinpath("test.html.jinja"), "w") as f:
        f.write("<html><head></head><body></body></html>")

    another_extra = tmp_path.joinpath("flood-html-test-templates-css")
    another_extra.mkdir(parents=True, exist_ok=True)
    with open(another_extra.joinpath("test.css.jinja"), "w") as f:
        f.write("body { background-color: red; }")

    multi_extra_loader = FHStylesLoader(extra_resources=[extra_template_path.as_posix(), another_extra.as_posix()])

    # Check that the styles loader is created correctly
    assert multi_extra_loader is not None
    # Check that the styles loader has the correct attributes
    assert hasattr(multi_extra_loader, "env")
    assert isinstance(multi_extra_loader.env, jinja2.environment.Environment)

    templates_path = resources.files("floods_html.styles")
    one_tmplt = (f for f in pathlib.Path(templates_path).glob("*") if not (f.name.endswith(".py") or f.is_dir()))
    multi_extra_loader.get_resource(next(one_tmplt).name)
    multi_extra_loader.get_resource("test.html.jinja")
    multi_extra_loader.get_resource("test.css.jinja")
    with pytest.raises(jinja2.TemplateNotFound):
        multi_extra_loader.get_resource("non_existent_template.css")
