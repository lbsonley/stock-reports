"""
Todo

Generate markdown pages with charts directly from data
https://florian-dahlitz.de/articles/generate-file-reports-using-pythons-template-class

"""
from pathlib import Path
import string


def make_report_returns(path_date, report_name):
    time_frames = ["1WK", "1Q", "1Y", "5Y"]
    reports_string = "\n"

    for time_frame in time_frames:
        reports_string += f'=== "{time_frame}"\n\n'
        reports_string += f'    {{{{ read_csv("../../assets/outperformers/returns/{path_date}/{report_name}-{time_frame.lower()}.csv", floatfmt=".1%") }}}}\n\n'

    return reports_string


def make_report_charts(symbols, path_date, report_name):
    time_frames = ["1WK", "1Q", "1Y", "5Y"]
    charts_string = "\n"
    for symbol in symbols:
        charts_string += f"### {symbol}\n\n"
        for time_frame in time_frames:
            charts_string += f'=== "{time_frame}"\n\n'
            charts_string += f"    ![{time_frame} - {symbol}](../../assets/outperformers/charts/{path_date}/{report_name}/{symbol}-{time_frame.lower()}.webp)\n\n"

    return charts_string


def make_report(date, category, report_name, symbols):
    publish_date = date.strftime("%Y-%m-%d")
    path_date = date.strftime("%y-%m-%d")

    Path(f"pages/posts/{path_date}").mkdir(parents=True, exist_ok=True)

    with open("lib/templates/index.md") as t:
        template = string.Template(t.read())

    final_output = template.substitute(
        publish_date=publish_date,
        path_date=path_date,
        title=f'{report_name.capitalize().replace("-", " ")} - {publish_date}',
        category=category,
        symbols=", ".join(symbols),
        charts=make_report_charts(symbols, path_date, report_name),
        returns=make_report_returns(path_date, report_name),
    )
    with open(f"pages/posts/{path_date}/{report_name}.md", "w") as output:
        output.write(final_output)
