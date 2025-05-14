from collections.abc import Iterable, Mapping
import os
from typing import List, Literal, Union, Optional, Dict, Any

from pydantic import BaseModel, model_validator
from pydantic_core import SchemaValidator

from floods_html.styles import FHStylesLoader


def check_schema(model: BaseModel) -> None:
    schema_validator = SchemaValidator(schema=model.__pydantic_core_schema__)
    schema_validator.validate_python(model.__dict__)


class FHBaseModel(BaseModel):
    html_options: Dict[str, Union[Dict[str, str], str, List[str]]] = {}

    def to_html(self, **kwargs) -> str:
        raise NotImplementedError(f"Model of type {type(self)} does not implement to_html() method.")


class FHTableEntry(FHBaseModel):
    value: Union[str, int, float, None]


class FHTableRow(FHBaseModel):
    data: List[FHTableEntry]


class FHTableHeader(FHBaseModel):
    data: List[FHTableRow] = []


class FHTableBody(FHBaseModel):
    data: List[FHTableRow] = []


class FHTable(FHBaseModel):
    title: str
    headers: FHTableHeader = FHTableHeader()
    rows: FHTableBody = FHTableBody()

    @model_validator(mode="after")
    def rows_wrong_size(self):
        header_lens = self.header_len()
        row_lens = self.rows_len()
        if len(header_lens) != 0 and len(row_lens) != 0:
            for row_len in row_lens:
                for header_len in header_lens:
                    if row_len != header_len:
                        raise ValueError("Not all row lengths match header lengths.")
        return self

    def header_len(self):
        lengths = []
        for header in self.headers.data:
            length = 0
            for entry in header.data:
                col_span = 1 if entry.html_options is None else int(entry.html_options.get("colspan", 1))
                length += col_span
            lengths.append(length)
        return lengths

    def rows_len(self):
        lengths = []
        for row in self.rows.data:
            length = 0
            for entry in row.data:
                col_span = 1 if entry.html_options is None else int(entry.html_options.get("colspan", 1))
                length += col_span
            lengths.append(length)
        return lengths

    def add_row(self, row: List[FHTableEntry], html_options: Optional[Dict[str, Union[Dict[str, str], str]]] = {}):
        self.rows.data.append(FHTableRow(data=row, html_options=html_options))
        check_schema(self)

    def add_header(
        self, header: List[FHTableEntry], html_options: Optional[Dict[str, Union[Dict[str, str], str]]] = {}
    ):
        self.headers.data.append(FHTableRow(data=header, html_options=html_options))
        check_schema(self)

    def to_html(self, **kwargs) -> str:
        html_template = "<{html_tag}{html_options}>{value}</{html_tag}>"

        def html_options_to_str(x: Mapping[Mapping[str, Any]]):
            tmplt = " {0}={1}"
            res = ""
            for k, v in x.items():
                if isinstance(v, str):
                    entry = tmplt.format(k, v)
                elif isinstance(v, Mapping):
                    entry = tmplt.format(k, '"' + "".join([f"{a}:{b}; " for a, b in v.items()]) + '"')
                elif isinstance(v, Iterable):
                    entry = tmplt.format(k, '"' + " ".join(v) + '"')
                else:
                    raise ValueError(f"Can't parse html_options '{k}:{v}' of type '{type(v)}'")
                res += entry
            return res

        table_row_str = ""
        for table_row in self.headers.data:
            table_entry_str = ""
            for header_entry in table_row.data:
                table_entry_str += html_template.format(
                    html_tag="th", html_options=html_options_to_str(header_entry.html_options), value=header_entry.value
                )
            table_row_str += html_template.format(
                html_tag="tr", html_options=html_options_to_str(table_row.html_options), value=table_entry_str
            )
        table_header_str = html_template.format(
            html_tag="thead", html_options=html_options_to_str(self.headers.html_options), value=table_row_str
        )

        table_row_str = ""
        for table_row in self.rows.data:
            table_entry_str = ""
            for table_entry in table_row.data:
                table_entry_str += html_template.format(
                    html_tag="td", html_options=html_options_to_str(table_entry.html_options), value=table_entry.value
                )
            table_row_str += html_template.format(
                html_tag="tr", html_options=html_options_to_str(table_row.html_options), value=table_entry_str
            )
        table_body_str = html_template.format(
            html_tag="tbody", html_options=html_options_to_str(self.rows.html_options), value=table_row_str
        )

        table_str = html_template.format(
            html_tag="table",
            html_options=html_options_to_str(self.html_options),
            value=table_header_str + table_body_str,
        )

        title_str = html_template.format(html_tag="h3", html_options="", value=self.title)

        return title_str + table_str


class FHFigure(BaseModel):
    title: str
    filename: str
    linked: bool = False

    def to_html(self, resources_root: str = None) -> str:
        if self.linked:
            figure_html_template = """
                <span>
                    <h4>{title}</h4>
                    <img src={imgname}/>
                </span>
            """

            figure_html = figure_html_template.format(
                title=self.title,
                imgname=self.filename,
            )
        else:
            resources_root = resources_root if resources_root is not None else ""
            svg_file = os.path.join(resources_root, self.filename)

            figure_html_template = """
            <div>
                <span>
                    <h4>{title}</h4>
                    {svg}
                </span>
            </div>
            """

            svg_contents = open(svg_file, "r").read()

            figure_html = figure_html_template.format(
                title=self.title,
                svg=svg_contents,
            )

        return figure_html


class FHStyleSheet(BaseModel):
    name: str
    linked: bool = False

    def to_html(self, resources_root=None) -> str:
        if self.linked:
            return f'<link rel="stylesheet" type="text/css" href="{self.name}">\n'

        else:
            resources_loader = FHStylesLoader(resources_root)
            tmplt = resources_loader.get_resource(self.name)
            with open(tmplt.filename, "r") as f:
                css = f.read()
            return "\n<style>{}\n</style>\n".format(css)


class FHObject(BaseModel):
    type: Literal["table", "svg_figure", "stylesheet"]
    data: Union[FHTable, FHFigure, FHStyleSheet]

    def to_html(self, **kwargs) -> str:
        return self.data.to_html(**kwargs)


class FHJson(BaseModel):
    data: List[FHObject] = []

    def add_table(self, table):
        self.data.append(FHObject(type="table", data=table))
        check_schema(self)

    def add_svg_figure(self, figure):
        self.data.append(FHObject(type="svg_figure", data=figure))
        check_schema(self)

    def add_stylesheet(self, stylesheet):
        self.data.append(FHObject(type="stylesheet", data=stylesheet))
        check_schema(self)

    def add(self, obj: FHObject | FHTable | FHFigure | FHStyleSheet):
        if isinstance(obj, FHTable):
            self.add_table(obj)
        elif isinstance(obj, FHFigure):
            self.add_svg_figure(obj)
        elif isinstance(obj, FHStyleSheet):
            self.add_stylesheet(obj)
        elif isinstance(obj, FHObject):
            self.data.append(obj)
            check_schema(self)
        else:
            raise ValueError("object of type {} not supported".format(type(obj)))


__all__ = [
    "FHTableEntry",
    "FHTableRow",
    "FHTableHeader",
    "FHTableBody",
    "FHTable",
    "FHFigure",
    "FHStyleSheet",
    "FHObject",
    "FHJson",
]
