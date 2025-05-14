import argparse
import json
import os

from .floods_html import json_to_html


def cli():
    parser = argparse.ArgumentParser(description="Convert JSON to HTML.")
    parser.add_argument("file_path", help="Input JSON file path.", metavar="FILE")
    parser.add_argument(
        "--local_resources",
        type=str,
        nargs="*",
        help="Location of optional resources for direct embedding in final HTML body.",
        metavar="DIR",
    )
    parser.add_argument("--outdir", default=os.getcwd(), help="Output path to generated HTML file. Defaults to FILE")
    args = parser.parse_args()

    with open(args.file_path, "r") as f:
        input_data = json.load(f)

    html_output = json_to_html(input_data, args.local_resources)

    # create outputs as files
    outname = os.path.basename(args.file_path)
    outdir = args.outdir
    outname = ".".join(os.path.splitext(outname)[:1])
    html_outfile = f"{outname}.html"
    with open(os.path.join(outdir, html_outfile), "w") as f:
        for html in html_output:
            f.write(html)


if __name__ == "__main__":
    cli()
