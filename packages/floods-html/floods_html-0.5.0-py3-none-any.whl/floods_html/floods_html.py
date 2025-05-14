from collections.abc import Iterable

from floods_html import json_format as jf


def json_to_html(input, resources_root: Iterable[str] | str | None = None):
    """
    Converts a flooding JSON object to flooding HTML object.

    Parameters
    ----------
    input : str or dict or FHJson
        Input JSON object.
    resources_root : str
        Local path to load any extra resources for direct embedding in the HTML body.

    Returns
    -------
    html_output : List[str]
        List of HTML strings for each entry in the JSON object.

    """
    if type(input) is str:
        pydantic_data_object = jf.FHJson.model_validate_json(input)
    elif type(input) is dict:
        pydantic_data_object = jf.FHJson(**input)
    elif isinstance(input, jf.FHJson):
        pydantic_data_object = input
    else:
        raise ValueError("Invalid input type. Must be either a JSON string, JSON object, or a FHJson class instance.")
    html_output = []
    for entry in pydantic_data_object.data:
        html_entry = entry.to_html(resources_root=resources_root)
        html_output.append(html_entry)
    return html_output
