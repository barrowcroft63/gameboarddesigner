#!/usr/bin/python3

#  type: ignore

from functools import partial
from tkinter import Menu
from typing import Callable

#  Recent files menu.

RECENT_FILES = "config.dat"


class RecentFiles:
    def __init__(
        self, recent_files: list[str], recent_files_menu: Menu, on_open_recent: Callable
    ) -> None:
        self.recent_files: list[str] = recent_files
        self.recent_files_menu: Menu = recent_files_menu
        self.on_open_recent: Callable = on_open_recent

    def load_recent_files(self) -> None:
        try:
            with open(RECENT_FILES, "r") as _file:
                _files: list[str] = _file.readlines()
                for _file in _files:
                    self.recent_files.append(_file.strip("\n"))
                    self.build_recent_items_menu()
        except FileNotFoundError:
            self.recent_files = []

    def save_recent_files(self) -> None:
        with open(RECENT_FILES, "w") as _file:
            for _recent_file in self.recent_files:
                _file.write(_recent_file)
                _file.write("\n")

    def build_recent_items_menu(self) -> None:

        if self.recent_files_menu.index("end") > 1:
            self.recent_files_menu.delete(0, self.recent_files_menu.index("end") - 2)

        for _recent_file in sorted(self.recent_files):
            _index: int = self.recent_files_menu.index("end") - 1
            self.recent_files_menu.insert_command(
                index=_index,
                label=_recent_file,
                command=partial(self.on_open_recent, _recent_file),
            )

    def clear_recent_files_list(self) -> None:

        self.recent_files = []
        self.save_recent_files()
        if self.recent_files_menu.index("end") > 1:
            self.recent_files_menu.delete(0, self.recent_files_menu.index("end") - 2)

    def add_to_recent_files_list(self, filename: str) -> None:

        if not filename in self.recent_files:
            self.recent_files.append(filename)
            self.build_recent_items_menu()
            self.save_recent_files()
