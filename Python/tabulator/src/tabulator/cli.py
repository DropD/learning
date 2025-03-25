import click
import pathlib

from tabulator import note_graph, tab_graph


@click.command("tabulator")
@click.argument("input-file", type=click.Path(is_file=True))
def main(input_file: pathlib.Path):
    notes = note_graph.build_from_file(input_file)
    tabs = tab_graph.build_from_notes(notes)
    click.echo(tab_graph.best_guess(tabs))
