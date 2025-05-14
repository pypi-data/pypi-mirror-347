import pytest
import floods_html as fh
import html5lib


def serialize(fragment):
    return html5lib.serializer.serialize(
        fragment,
        encoding="utf-8",
        omit_optional_tags=False,
        quote_attr_values="spec",
        strip_whitespace=True,
    )


@pytest.mark.parametrize(
    "export_type",
    ["str", "dict", "object"],
)
def test_valid_html_default_construction(tmp_path, json_example, export_type):
    if export_type == "str":
        exported_object = json_example.json_obj.model_dump_json()
    elif export_type == "dict":
        exported_object = json_example.json_obj.model_dump()
    elif export_type == "object":
        exported_object = json_example.json_obj

    html5parser = html5lib.HTMLParser(strict=True)
    with open(tmp_path.joinpath("result.html"), "wb") as fout:
        for jentry, html in enumerate(fh.json_to_html(exported_object, **json_example.to_html_kwargs)):
            frag = html5parser.parseFragment(html)
            serialized = serialize(frag)
            fout.write(serialized)
            assert serialize(html5parser.parseFragment(json_example.expected_html[jentry])) == serialized


@pytest.mark.parametrize("export_type", ["str", "dict", "object"])
def test_valid_html_manual_construction(export_type):
    json_object = fh.FHJson()
    figure = fh.FHFigure(title="Test Figure", filename="https://website/test.svg", linked=True)
    json_object.add_svg_figure(figure)
    table = fh.FHTable(title="Table One")
    table.add_header(
        [
            fh.FHTableEntry(value=40, html_options={"style": {"background-color": "FFFFFF"}}),
            fh.FHTableEntry(value="Name"),
        ]
    )
    table.add_row([fh.FHTableEntry(value="540", html_options={"class": "test"}), fh.FHTableEntry(value=None)])
    table.add_row([fh.FHTableEntry(value="540", html_options={"id": "test1 test2"}), fh.FHTableEntry(value=670)])
    json_object.add_table(table)

    if export_type == "str":
        exported_object = json_object.model_dump_json()
    elif export_type == "dict":
        exported_object = json_object.model_dump()
    elif export_type == "object":
        exported_object = json_object

    # TODO: implement and test HTML generation
    html5parser = html5lib.HTMLParser(strict=True)
    for html in fh.json_to_html(exported_object):
        html5parser.parseFragment(html)
