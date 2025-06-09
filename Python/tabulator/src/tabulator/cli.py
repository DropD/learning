import pathlib

import click

from tabulator.notes import note_graph
from tabulator.tabulature import tab_graph


@click.command("tabulator")
@click.argument(
    "input-file",
    type=click.Path(file_okay=True, dir_okay=False, path_type=pathlib.Path),
)
def main(input_file: pathlib.Path):
    notes = note_graph.build_from_file(input_file)
    tabs = tab_graph.build_from_notes(notes)
    tab_graph.txt_tab_echo_all(tabs)
    # click.echo(tab_graph.best_guess(tabs))
