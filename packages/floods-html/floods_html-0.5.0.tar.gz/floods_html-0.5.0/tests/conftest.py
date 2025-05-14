from io import StringIO
from dataclasses import dataclass, field

from floods_html import FHTable, FHTableHeader, FHTableRow, FHTableEntry, FHTableBody
from floods_html import FHJson, FHObject, FHFigure, FHStyleSheet
from pytest import fixture


@dataclass
class JSONTestExample:
    """Struct-like class to hold JSON test examples, with expected outcomes for each component."""

    json_obj: FHObject | list[FHObject]
    expected_html: str | list[str]
    to_html_kwargs: dict | list[dict] = field(default_factory=dict)


@fixture
def tmp_resources_path(tmp_path):
    """
    Fixture to provide a temporary path for resources.
    """
    tmp_resources_path = tmp_path.joinpath("flood-html-test-templates")
    tmp_resources_path.mkdir(parents=True, exist_ok=True)
    return tmp_resources_path


@fixture
def dummy_svg_figure_data():
    """
    Fixture to provide a simple raw SVG plot example.
    """
    figdata = StringIO("""
        <svg xmlns="http://www.w3.org/2000/svg" width="400" height="200">
            <rect width="100%" height="100%" fill="white"/>
            <g>
                <line x1="50" y1="150" x2="350" y2="150" stroke="black" stroke-width="2"/>
                <line x1="50" y1="150" x2="50" y2="50" stroke="black" stroke-width="2"/>
                <circle cx="100" cy="120" r="5" fill="red"/>
                <circle cx="150" cy="100" r="5" fill="red"/>
                <circle cx="200" cy="80" r="5" fill="red"/>
                <circle cx="250" cy="60" r="5" fill="red"/>
                <circle cx="300" cy="90" r="5" fill="red"/>
                <polyline points="100,120 150,100 200,80 250,60 300,90" fill="none" stroke="red" stroke-width="2"/>
                <text x="200" y="180" font-size="12" text-anchor="middle">Time</text>
                <text x="20" y="100" font-size="12" text-anchor="middle" transform="rotate(-90, 20, 100)">Value</text>
            </g>
        </svg>
    """)
    return figdata


@fixture
def dummy_svg_figure(tmp_resources_path, dummy_svg_figure_data):
    """
    Fixture to provide a dummy SVG figure object.
    """
    fname = "test.svg"
    svg_path = tmp_resources_path.joinpath(fname)

    with open(svg_path, "w") as f:
        conts = dummy_svg_figure_data.read()
        f.write(conts)

    return JSONTestExample(
        json_obj=FHObject(type="svg_figure", data=FHFigure(title="Test Figure", filename=fname, linked=False)),
        expected_html=" <div> <span> <h4>Test Figure</h4>" + conts + "</span> </div> ",
        to_html_kwargs={"resources_root": tmp_resources_path.as_posix()},
    )


@fixture
def stylesheet():
    return {
        "name": "test.css",
        "content": ["body { background-color: #5ca876; }", "table { border-width: 1px; border-style: solid; }"],
    }


@fixture
def dummy_stylesheet(stylesheet):
    """
    Fixture to provide a dummy stylesheet object.
    """
    return JSONTestExample(
        json_obj=FHObject(type="stylesheet", data=FHStyleSheet(name=stylesheet["name"])),
        expected_html=" <style>" + "".join(stylesheet["content"]) + "\n</style> ",
    )


@fixture
def styles_resources(tmp_resources_path, stylesheet):
    """
    Fixture to load the template loader.
    """

    extra_template_path = tmp_resources_path
    with open(extra_template_path.joinpath(stylesheet["name"]), "w") as f:
        f.writelines(stylesheet["content"])

    return extra_template_path.as_posix()


@fixture
def merged_headers_table():
    table = FHTable(
        title="Table merged headers",
        headers=FHTableHeader(
            data=[
                FHTableRow(
                    data=[
                        FHTableEntry(value="Naming", html_options={"colspan": "3"}),
                    ]
                )
            ]
        ),
        rows=FHTableBody(
            data=[
                FHTableRow(
                    data=[
                        FHTableEntry(value="540", html_options={"style": {"background-color": "FFFFFF"}}),
                        FHTableEntry(value=None, html_options={"id": "test"}),
                        FHTableEntry(value=517863, html_options={"class": "test"}),
                    ]
                ),
            ]
        ),
    )
    exp = '<h3>Table merged headers</h3><table><thead><tr><th colspan=3>Naming</th></tr></thead><tbody><tr><td style="background-color:FFFFFF; ">540</td><td id=test>None</td><td class=test>517863</td></tr></tbody></table>'
    return JSONTestExample(json_obj=FHObject(type="table", data=table), expected_html=exp)


@fixture
def gridded2x2table():
    table = FHTable(
        title="Table 2x2",
        headers=FHTableHeader(
            data=[
                FHTableRow(
                    data=[
                        FHTableEntry(value=40, html_options={"style": {"background-color": "FFFFFF"}}),
                        FHTableEntry(value="Name", html_options={"style": {"background-color": "FFFFFF"}}),
                    ]
                )
            ]
        ),
        rows=FHTableBody(
            data=[
                FHTableRow(
                    data=[
                        FHTableEntry(value="540", html_options={"style": {"text-align": "center"}}),
                        FHTableEntry(value=None),
                    ]
                ),
                FHTableRow(
                    data=[
                        FHTableEntry(value="540", html_options={"style": {"background-color": "FF0000"}}),
                        FHTableEntry(value=670, html_options={"style": {"color": "FFFFFF"}}),
                    ]
                ),
            ]
        ),
    )
    exp = '<h3>Table 2x2</h3><table><thead><tr><th style="background-color:FFFFFF; ">40</th><th style="background-color:FFFFFF; ">Name</th></tr></thead><tbody><tr><td style="text-align:center; ">540</td><td>None</td></tr><tr><td style="background-color:FF0000; ">540</td><td style="color:FFFFFF; ">670</td></tr></tbody></table>'
    return JSONTestExample(json_obj=FHObject(type="table", data=table), expected_html=exp)


# ------------- Actual Json data fixtures -------------------
@fixture
def json_data_merged_headers_table_with_plain_svg(merged_headers_table, dummy_svg_figure):
    """
    Fixture to provide a JSON object for testing. Use `json_example` fixture to get all possible examples.
    """
    return JSONTestExample(
        [merged_headers_table.json_obj, dummy_svg_figure.json_obj],
        expected_html=[merged_headers_table.expected_html, dummy_svg_figure.expected_html],
        to_html_kwargs=dummy_svg_figure.to_html_kwargs,
    )


@fixture
def json_data_gridded_table_with_linked_figures(gridded2x2table):
    """
    Fixture to provide a JSON object for testing. Use `json_example` fixture to get all possible examples.
    """
    data = [
        FHObject(
            type="svg_figure",
            data=FHFigure(title=f"Test Figure {i}", filename=f"https://website/test{i}.svg", linked=True),
        )
        for i in range(1, 3)
    ]
    exp = [f" <span> <h4>Test Figure {i}</h4> <img src=https://website/test{i}.svg/> </span> " for i in range(1, 3)]
    data = [gridded2x2table.json_obj, *data]
    exp = [gridded2x2table.expected_html, *exp]
    return JSONTestExample(
        json_obj=data,
        expected_html=exp,
    )


@fixture
def json_data_merged_table_with_styles(request, dummy_stylesheet, styles_resources):
    """
    Fixture to provide a JSON object for testing. Use `json_example` fixture to get all possible examples.
    """
    plain_json = request.getfixturevalue("json_data_merged_headers_table_with_plain_svg")
    plain_json.json_obj.append(dummy_stylesheet.json_obj)
    plain_json.expected_html.append(dummy_stylesheet.expected_html)
    return JSONTestExample(
        json_obj=plain_json.json_obj,
        expected_html=plain_json.expected_html,
        to_html_kwargs=dict(resources_root=styles_resources),
    )


@fixture
def json_data_gridded_table_with_styles(request, dummy_stylesheet, styles_resources):
    """
    Fixture to provide a JSON object for testing. Use `json_example` fixture to get all possible examples.
    """
    plain_json = request.getfixturevalue("json_data_gridded_table_with_linked_figures")
    for entry in plain_json.json_obj:
        if isinstance(entry, FHFigure):
            entry.linked = False
    plain_json.json_obj.append(dummy_stylesheet.json_obj)
    plain_json.expected_html.append(dummy_stylesheet.expected_html)
    return JSONTestExample(
        json_obj=plain_json.json_obj,
        expected_html=plain_json.expected_html,
        to_html_kwargs=dict(resources_root=styles_resources),
    )


@fixture(
    params=[
        "json_data_merged_headers_table_with_plain_svg",
        "json_data_gridded_table_with_linked_figures",
        "json_data_gridded_table_with_styles",
        "json_data_merged_table_with_styles",
    ]
)
def json_example(request):
    """
    Fixture to provide different JSON objects for testing.
    """
    json_data = request.getfixturevalue(request.param)
    return JSONTestExample(
        json_obj=FHJson(data=json_data.json_obj),
        expected_html=json_data.expected_html,
        to_html_kwargs=json_data.to_html_kwargs,
    )
