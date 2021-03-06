"""Rich terminal frontend using `rich`."""

from datetime import timedelta
from shutil import get_terminal_size
import typing as t

from humanize import precisedelta  # type: ignore
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.table import Table
from rich.text import Text


def create_track_view(items: list[t.Mapping], *, columns: int = 3) -> Align:
    """Create a renderable view for tracks."""
    term_cols, _ = get_terminal_size()

    column_width = term_cols // columns - 1
    truncate_width = column_width - 10

    views = []
    for index, item in enumerate(items):
        track = item["track"]

        _name = Text(track["name"])
        _name.truncate(truncate_width, overflow="ellipsis")
        name = Columns(
            [
                Text(f"{index}."),
                _name,
            ]
        )

        _artists = ", ".join(artist["name"] for artist in track["artists"])
        artists = Text("Artists:", style="bold").append_text(
            Text(f" {_artists}", style="not bold")
        )
        artists.truncate(truncate_width, overflow="ellipsis")

        _duration = precisedelta(
            timedelta(milliseconds=track["duration_ms"]),
            format="%0.0f",
        )
        duration = f"[bold]Duration:[/bold] {_duration}"

        _album = track["album"]["name"]
        album = Text("Album:", style="bold").append_text(
            Text(f" {_album}", style="not bold")
        )
        album.truncate(truncate_width, overflow="ellipsis")

        view = Table(expand=True, box=box.SQUARE)

        view.add_column(name)
        view.add_row(artists)
        view.add_row(duration)
        view.add_row(album)

        views.append(view)

    return Align(Columns(views, width=column_width), align="center")


def create_album_view(items: list[t.Mapping], *, columns: int = 3) -> Align:
    """Create renderable views from albums."""
    term_cols, _ = get_terminal_size()

    column_width = term_cols // columns - 1
    truncate_width = column_width - 10

    views = []
    for index, item in enumerate(items):
        album = item["album"]

        _name = Text(album["name"])
        _name.truncate(truncate_width, overflow="ellipsis")
        name = Columns([Text(f"{index}."), _name])

        _label = album["label"]
        label = Text("Label:", style="bold").append_text(
            Text(f" {_label}", style="not bold")
        )
        label.truncate(truncate_width, overflow="ellipsis")

        _artists = ", ".join(artist["name"] for artist in album["artists"])
        artists = Text("Artists:", style="bold").append_text(
            Text(f" {_artists}", style="not bold")
        )
        artists.truncate(truncate_width, overflow="ellipsis")

        view = Table(expand=True, box=box.SQUARE)

        view.add_column(name)
        view.add_row(label)
        view.add_row(artists)

        views.append(view)

    return Align(Columns(views, width=column_width), align="center")
