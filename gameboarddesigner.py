#!/usr/bin/python3

#  type: ignore

from pathlib import Path
from tkinter import Menu
from typing import Optional

import pygubu.widgets.simpletooltip as tooltip
from CTkColorPicker import AskColor
from CTkMessagebox import CTkMessagebox
from customtkinter import (
    CENTER,
    CTk,
    CTkButton,
    CTkEntry,
    CTkFrame,
    CTkImage,
    CTkOptionMenu,
    CTkTabview,
    StringVar,
    filedialog,
)
from gameboard.gameboard import Gameboard
from PIL import Image, ImageTk
from pygubu import Builder

from recentfiles import RecentFiles
from validation import validated_colour, validated_int

PROJECT_PATH = Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gameboarddesigner.ui"


class GameboarddesignerApp:
    def __init__(self) -> None:

        #  Initialise the gameboard.

        self.gameboard: Gameboard = Gameboard()
        self.gameboard.cell_selected_callback = self.cell_selected
        self.filename: str = ""

        #  Initialisze the pygubu builder.

        self.builder: Builder = Builder()
        self.builder.add_resource_path(PROJECT_PATH)
        self.builder.add_from_file(PROJECT_UI)

        # Initialise main widget.

        self.mainwindow: CTk = self.builder.get_object("ctk")
        self.mainwindow.title("Gameboard Designer")

        self.mainwindow.after(0, lambda: self.mainwindow.state("zoomed"))
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.on_quit)

        # Initialise main menu.

        self.main_menu: Menu = self.builder.get_object("menu")
        self.mainwindow.configure(menu=self.main_menu)

        #  Get all objects.

        self.get_all_objects()

        #  Import all variables.

        self.import_all_variables()

        #  Connect all callbacks.

        self.connect_all_callbacks()

        #  Connect all accelerators.

        self.connect_all_accelerators()

        #  Initialise recent files list.

        self.initialise_recent_files_list()

        #  Initialise image cache.

        self.images: dict[str, ImageTk.PhotoImage] = {}

    def get_all_objects(self) -> None:

        self.main: CTkFrame = self.builder.get_object("main")
        self.palette: CTkTabview = self.builder.get_object("palette")
        self.recent_files_menu: Menu = self.builder.get_object("recent_files_menu")

        #  Details tab.

        self.name: CTkEntry = self.builder.get_object("name")
        tooltip.create(
            self.name,
            "Sets the name of the gameboard.",
        )
        self.version: CTkEntry = self.builder.get_object("version")
        tooltip.create(
            self.version,
            "Sets the version of the gameboard.",
        )
        self.date: CTkEntry = self.builder.get_object("date")
        tooltip.create(
            self.date,
            "Sets the date of the gameboard.",
        )
        self.author: CTkEntry = self.builder.get_object("author")
        tooltip.create(
            self.author,
            "Sets the author of the gameboard.",
        )

        #  Boarders tab.

        self.width_of_left_outer_boarder: CTkEntry = self.builder.get_object(
            "width_of_left_outer_boarder"
        )
        tooltip.create(
            self.width_of_left_outer_boarder,
            "Sets the width of the left outer boarder.",
        )
        self.width_of_top_outer_boarder: CTkEntry = self.builder.get_object(
            "width_of_top_outer_boarder"
        )
        tooltip.create(
            self.width_of_top_outer_boarder, "Sets the width of the top outer boarder."
        )
        self.width_of_right_outer_boarder: CTkEntry = self.builder.get_object(
            "width_of_right_outer_boarder"
        )
        tooltip.create(
            self.width_of_right_outer_boarder,
            "Sets the width of the right outer boarder.",
        )
        self.width_of_bottom_outer_boarder: CTkEntry = self.builder.get_object(
            "width_of_bottom_outer_boarder"
        )
        tooltip.create(
            self.width_of_bottom_outer_boarder,
            "Sets the width of the bottom outer boarder.",
        )
        self.all_outer_width: CTkButton = self.builder.get_object("all_outer_width")
        tooltip.create(
            self.all_outer_width,
            "Sets the width of all outer boarders to this value.",
        )
        self.colour_of_outer_boarder: CTkEntry = self.builder.get_object(
            "colour_of_outer_boarder"
        )
        tooltip.create(
            self.colour_of_outer_boarder,
            "Sets the colour of the outer boarder.",
        )
        self.pick_outer_boarder_colour: CTkButton = self.builder.get_object(
            "pick_outer_boarder_colour"
        )
        tooltip.create(
            self.pick_outer_boarder_colour,
            "Picks a colour for the outer boarder.",
        )

        self.width_of_left_inner_boarder: CTkEntry = self.builder.get_object(
            "width_of_left_inner_boarder"
        )
        tooltip.create(
            self.width_of_left_inner_boarder,
            "Sets the width of the left inner boarder.",
        )
        self.width_of_top_inner_boarder: CTkEntry = self.builder.get_object(
            "width_of_top_inner_boarder"
        )
        tooltip.create(
            self.width_of_top_inner_boarder,
            "Sets the width of the top inner boarder.",
        )
        self.width_of_right_inner_boarder: CTkEntry = self.builder.get_object(
            "width_of_right_inner_boarder"
        )
        tooltip.create(
            self.width_of_right_inner_boarder,
            "Sets the width of the right inner boarder.",
        )
        self.width_of_bottom_inner_boarder: CTkEntry = self.builder.get_object(
            "width_of_bottom_inner_boarder"
        )
        tooltip.create(
            self.width_of_bottom_inner_boarder,
            "Sets the width of the bottom inner boarder.",
        )
        self.all_inner_width: CTkButton = self.builder.get_object("all_inner_width")
        tooltip.create(
            self.all_inner_width,
            "Sets the width of all inner boarders to this value.",
        )
        self.colour_of_inner_boarder: CTkEntry = self.builder.get_object(
            "colour_of_inner_boarder"
        )
        tooltip.create(
            self.colour_of_inner_boarder,
            "Sets the colour of the inner boarder.",
        )
        self.pick_inner_boarder_colour: CTkButton = self.builder.get_object(
            "pick_inner_boarder_colour"
        )
        tooltip.create(
            self.pick_inner_boarder_colour,
            "Picks a colour for the inner boarder.",
        )

        #  Cells tab.

        self.number_of_cells_horizontally: CTkEntry = self.builder.get_object(
            "number_of_cells_horizontally"
        )
        tooltip.create(
            self.number_of_cells_horizontally,
            "Sets the number of cells horizontally.",
        )
        self.number_of_cells_vertically: CTkEntry = self.builder.get_object(
            "number_of_cells_vertically"
        )
        tooltip.create(
            self.number_of_cells_vertically,
            "Sets the number of cells vertically.",
        )

        self.cells_on_rows_row: CTkEntry = self.builder.get_object("cells_on_rows_row")
        tooltip.create(
            self.cells_on_rows_row,
            "The number (zero indexed) of the selected row.",
        )

        self.height_of_cell: CTkEntry = self.builder.get_object("height_of_cell")
        tooltip.create(
            self.height_of_cell,
            "Sets the height of the cells on the selected row.",
        )
        self.all_rows_height: CTkButton = self.builder.get_object("all_rows_height")
        tooltip.create(
            self.all_rows_height,
            "Sets the height of the cells on all rows to this value.",
        )
        self.top_padding_of_cell: CTkEntry = self.builder.get_object(
            "top_padding_of_cell"
        )
        tooltip.create(
            self.top_padding_of_cell,
            "Sets the top padding of the cells on the selected row.",
        )
        self.all_rows_top: CTkButton = self.builder.get_object("all_rows_top")
        tooltip.create(
            self.all_rows_top,
            "Sets the top padding of the cells on all rows to this value.",
        )
        self.bottom_padding_of_cell: CTkEntry = self.builder.get_object(
            "bottom_padding_of_cell"
        )
        tooltip.create(
            self.bottom_padding_of_cell,
            "Sets the bottom padding of the cells on the selected row.",
        )
        self.all_rows_bottom: CTkButton = self.builder.get_object("all_rows_bottom")
        tooltip.create(
            self.all_rows_bottom,
            "Sets the bottom padding of the cells on all rows to this value.",
        )
        self.size_of_horizontal_gutter_after_cell: CTkEntry = self.builder.get_object(
            "size_of_horizontal_gutter_after_cell"
        )
        tooltip.create(
            self.size_of_horizontal_gutter_after_cell,
            "Sets the size of the horizontal gutter after the selected row.",
        )
        self.all_rows_horizontal_gutter: CTkButton = self.builder.get_object(
            "all_rows_horizontal_gutter"
        )
        tooltip.create(
            self.all_rows_horizontal_gutter,
            "Sets the size of the horizontal gutter following all rows to this value.",
        )

        self.cells_on_columns_column: CTkEntry = self.builder.get_object(
            "cells_on_columns_column"
        )
        tooltip.create(
            self.cells_on_columns_column,
            "The number (zero indexed) of the selected column.",
        )

        self.width_of_cell: CTkEntry = self.builder.get_object("width_of_cell")
        tooltip.create(
            self.width_of_cell,
            "Sets the width of the cells on the selected column.",
        )
        self.all_columns_width: CTkButton = self.builder.get_object("all_columns_width")
        tooltip.create(
            self.all_columns_width,
            "Sets the width of the cells on all columns to this value.",
        )
        self.left_padding_of_cell: CTkEntry = self.builder.get_object(
            "left_padding_of_cell"
        )
        tooltip.create(
            self.left_padding_of_cell,
            "Sets the left padding of the cells on the selected column.",
        )
        self.all_columns_left: CTkButton = self.builder.get_object("all_columns_left")
        tooltip.create(
            self.all_columns_left,
            "Sets the left padding of the cells on all columns to this value.",
        )
        self.right_padding_of_cell: CTkEntry = self.builder.get_object(
            "right_padding_of_cell"
        )
        tooltip.create(
            self.right_padding_of_cell,
            "Sets the right padding of the cells on the selected column.",
        )
        self.all_columns_right: CTkButton = self.builder.get_object("all_columns_right")
        tooltip.create(
            self.all_columns_right,
            "Sets the right padding of the cells on all columns to this value.",
        )
        self.size_of_vertical_gutter_after_cell: CTkEntry = self.builder.get_object(
            "size_of_vertical_gutter_after_cell"
        )
        tooltip.create(
            self.size_of_vertical_gutter_after_cell,
            "Sets the size of the vertical gutter after the selected column.",
        )
        self.all_columns_vertical_gutter: CTkButton = self.builder.get_object(
            "all_columns_vertical_gutter"
        )
        tooltip.create(
            self.all_columns_vertical_gutter,
            "Sets the size of the vertical gutter following all columns to this value.",
        )
        self.colour_of_cell_gutter: CTkEntry = self.builder.get_object(
            "colour_of_cell_gutter"
        )
        tooltip.create(
            self.colour_of_cell_gutter,
            "Sets the colour of the cell gutter.",
        )
        self.pick_gutter_colour: CTkButton = self.builder.get_object(
            "pick_gutter_colour"
        )
        tooltip.create(
            self.pick_gutter_colour,
            "Picks a colour for the cell gutter.",
        )

        self.cells_on_rows_columns_row: CTkEntry = self.builder.get_object(
            "cells_on_rows_columns_row"
        )
        tooltip.create(
            self.cells_on_rows_columns_row,
            "The number (zero indexed) of the selected row.",
        )

        self.cells_on_rows_columns_column: CTkEntry = self.builder.get_object(
            "cells_on_rows_columns_column"
        )
        tooltip.create(
            self.cells_on_rows_columns_column,
            "The number (zero indexed) of the selected column.",
        )

        self.colour_of_cell: CTkEntry = self.builder.get_object("colour_of_cell")
        tooltip.create(
            self.colour_of_cell,
            "Sets the colour of the cell on the selected row and column.",
        )

        self.all_cell_colour: CTkEntry = self.builder.get_object("all_cell_colour")
        tooltip.create(
            self.all_cell_colour, "Sets the cell colour of all cells to this value."
        )
        self.pick_cell_colour: CTkEntry = self.builder.get_object("pick_cell_colour")
        tooltip.create(
            self.pick_cell_colour,
            "Picks a colour for the cell on the selected row and column.",
        )

        self.colour_of_cell_padding: CTkEntry = self.builder.get_object(
            "colour_of_cell_padding"
        )
        tooltip.create(
            self.colour_of_cell_padding,
            "Sets the colour of the cell padding on the selected row and column.",
        )
        self.all_cell_padding_colour: CTkEntry = self.builder.get_object(
            "all_cell_padding_colour"
        )
        tooltip.create(
            self.all_cell_padding_colour,
            "Sets the cell padding colour of all cells to this value.",
        )
        self.pick_cell_padding_colour: CTkEntry = self.builder.get_object(
            "pick_cell_padding_colour"
        )
        tooltip.create(
            self.pick_cell_padding_colour,
            "Picks a colour for the padding for the cell on the selected row and column.",
        )

        #  Decorators tab.

        self.cell_light_colour: CTkEntry = self.builder.get_object("cell_light_colour")
        tooltip.create(
            self.cell_light_colour,
            "Sets the colour for the light cells in the checkerboard pattern.",
        )
        self.pick_cell_light_colour: CTkEntry = self.builder.get_object(
            "pick_cell_light_colour"
        )
        tooltip.create(
            self.pick_cell_light_colour,
            "Picks a colour for the light cells in the checkerboard pattern.",
        )

        self.cell_dark_colour: CTkEntry = self.builder.get_object("cell_dark_colour")
        tooltip.create(
            self.cell_dark_colour,
            "Sets the colour for the dark cells in the checkerboard pattern.",
        )
        self.pick_cell_dark_colour: CTkEntry = self.builder.get_object(
            "pick_cell_dark_colour"
        )
        tooltip.create(
            self.pick_cell_dark_colour,
            "Picks a colour for the dark cells in the checkerboard pattern.",
        )
        self.apply_checkerboard: CTkEntry = self.builder.get_object(
            "apply_checkerboard"
        )
        tooltip.create(
            self.apply_checkerboard,
            "Applies a checkerboard pattern to the current gameboard.",
        )

        self.cell_decorators_row: CTkEntry = self.builder.get_object(
            "cell_decorators_row"
        )
        tooltip.create(
            self.cell_decorators_row, "The number (zero indexed) of the selected row."
        )

        self.cell_decorators_column: CTkEntry = self.builder.get_object(
            "cell_decorators_column"
        )
        tooltip.create(
            self.cell_decorators_column,
            "The number (zero indexed) of the selected column.",
        )
        self.cell_decorator: CTkEntry = self.builder.get_object("cell_decorator")
        tooltip.create(
            self.cell_decorator,
            "The filename of the decorator for the cell at the selected row and column.",
        )
        self.pick_cell_decorator: CTkEntry = self.builder.get_object(
            "pick_cell_decorator"
        )
        tooltip.create(
            self.pick_cell_decorator,
            "Pick the decorator for the cell at the selected row and column.",
        )
        self.remove_cell_decorator: CTkEntry = self.builder.get_object(
            "remove_cell_decorator"
        )
        tooltip.create(
            self.remove_cell_decorator,
            "Removes the decorator from the cell at the selected row and column.",
        )

        self.board_decorator_choice: CTkOptionMenu = self.builder.get_object(
            "board_decorator_choice"
        )
        tooltip.create(
            self.board_decorator_choice,
            "Selects a board decorator.",
        )

        self.board_decorator: CTkEntry = self.builder.get_object("board_decorator")
        tooltip.create(
            self.board_decorator,
            "The filename of the board decorator.",
        )

        self.pick_board_decorator: CTkButton = self.builder.get_object(
            "pick_board_decorator"
        )
        tooltip.create(
            self.pick_board_decorator,
            "Picks a board decorator.",
        )

        self.board_decorator_x_pos: CTkEntry = self.builder.get_object(
            "board_decorator_x_pos"
        )
        tooltip.create(
            self.board_decorator_x_pos,
            "Sets the horizontal position of the board decorator.",
        )
        self.board_decorator_y_pos: CTkEntry = self.builder.get_object(
            "board_decorator_y_pos"
        )
        tooltip.create(
            self.board_decorator_y_pos,
            "Sets the vertical position of the board decorator.",
        )
        self.remove_board_decorator: CTkButton = self.builder.get_object(
            "remove_board_decorator"
        )
        tooltip.create(
            self.remove_board_decorator,
            "Removes the board decorator.",
        )

        #  Tokens tab.

        self.token_choice: CTkOptionMenu = self.builder.get_object("token_choice")
        tooltip.create(
            self.token_choice,
            "Selects a token to edit.",
        )

        self.token_name: CTkButton = self.builder.get_object("token_name")
        tooltip.create(
            self.token_name,
            "Sets the name of the token.",
        )

        self.token: CTkButton = self.builder.get_object("token")
        tooltip.create(
            self.token,
            "The filename of the token.",
        )

        self.pick_token: CTkButton = self.builder.get_object("pick_token")
        tooltip.create(
            self.pick_token,
            "Picks a token.",
        )

        self.remove_token: CTkButton = self.builder.get_object("remove_token")
        tooltip.create(
            self.remove_token,
            "Removes a token.",
        )

        self.placed_tokens_row: CTkButton = self.builder.get_object("placed_tokens_row")
        tooltip.create(
            self.placed_tokens_row,
            "The number (zero indexed) of the selected row.",
        )

        self.placed_tokens_column: CTkButton = self.builder.get_object(
            "placed_tokens_column"
        )
        tooltip.create(
            self.placed_tokens_column,
            "The number (zero indexed) of the selected column.",
        )

        self.placed_token_name_choice: CTkButton = self.builder.get_object(
            "placed_token_name_choice"
        )
        tooltip.create(
            self.placed_token_name_choice,
            "Selects a token to place.",
        )

        self.remove_placed_token: CTkButton = self.builder.get_object(
            "remove_placed_token"
        )
        tooltip.create(
            self.remove_placed_token,
            "Removes the token at the selected row and column",
        )

    def import_all_variables(self) -> None:

        self.var_name: StringVar = None
        self.var_version: StringVar = None
        self.var_date: StringVar = None
        self.var_author: StringVar = None

        self.var_width_of_left_outer_boarder: StringVar = None
        self.var_width_of_top_outer_boarder: StringVar = None
        self.var_width_of_right_outer_boarder: StringVar = None
        self.var_width_of_bottom_outer_boarder: StringVar = None
        self.var_colour_of_outer_boarder: StringVar = None
        self.var_width_of_left_inner_boarder: StringVar = None
        self.var_width_of_top_inner_boarder: StringVar = None
        self.var_width_of_right_inner_boarder: StringVar = None
        self.var_width_of_bottom_inner_boarder: StringVar = None
        self.var_colour_of_inner_boarder: StringVar = None

        self.var_number_of_cells_horizontally: StringVar = None
        self.var_number_of_cells_vertically: StringVar = None

        self.var_cells_on_rows_row: StringVar = None
        self.var_height_of_cell: StringVar = None
        self.var_top_padding_of_cell: StringVar = None
        self.var_bottom_padding_of_cell: StringVar = None
        self.var_size_of_horizontal_gutter_after_cell: StringVar = None

        self.var_cells_on_columns_column: StringVar = None
        self.var_width_of_cell: StringVar = None
        self.var_left_padding_of_cell: StringVar = None
        self.var_right_padding_of_cell: StringVar = None
        self.var_size_of_vertical_gutter_after_cell: StringVar = None
        self.var_colour_of_cell_gutter: StringVar = None

        self.var_colour_of_cell_gutter: StringVar = None

        self.var_cells_on_rows_columns_row: StringVar = None
        self.var_cells_on_rows_columns_column: StringVar = None
        self.var_colour_of_cell: StringVar = None
        self.var_colour_of_cell_padding: StringVar = None

        self.var_cell_light_colour: StringVar = None
        self.var_cell_dark_colour: StringVar = None

        self.var_cell_decorators_row: StringVar = None
        self.var_cell_decorators_column: StringVar = None
        self.var_cell_decorator: StringVar = None

        self.var_board_decorator_choice: StringVar = None
        self.var_board_decorator: StringVar = None
        self.var_board_decorator_x_pos: StringVar = None
        self.var_board_decorator_y_pos: StringVar = None

        self.var_token_choice: StringVar = None
        self.var_token_name: StringVar = None
        self.var_token: StringVar = None

        self.var_placed_tokens_row: StringVar = None
        self.var_placed_tokens_column: StringVar = None
        self.var_placed_token_name_choice: StringVar = None

        self.builder.import_variables(self)

    def connect_all_callbacks(self) -> None:

        #  Connect callbacks  - <FocusOut>

        self.builder.connect_callbacks(self)

        self.name.bind("<FocusOut>", self.on_name_changed)
        self.version.bind("<FocusOut>", self.on_version_changed)
        self.date.bind("<FocusOut>", self.on_date_changed)
        self.author.bind("<FocusOut>", self.on_author_changed)

        self.width_of_left_outer_boarder.bind(
            "<FocusOut>", self.on_width_of_left_outer_boarder_changed
        )
        self.width_of_top_outer_boarder.bind(
            "<FocusOut>", self.on_width_of_top_outer_boarder_changed
        )
        self.width_of_right_outer_boarder.bind(
            "<FocusOut>", self.on_width_of_right_outer_boarder_changed
        )
        self.width_of_bottom_outer_boarder.bind(
            "<FocusOut>", self.on_width_of_bottom_outer_boarder_changed
        )
        self.colour_of_outer_boarder.bind(
            "<FocusOut>", self.on_colour_of_outer_boarder_changed
        )

        self.width_of_left_inner_boarder.bind(
            "<FocusOut>", self.on_width_of_left_inner_boarder_changed
        )
        self.width_of_top_inner_boarder.bind(
            "<FocusOut>", self.on_width_of_top_inner_boarder_changed
        )
        self.width_of_right_inner_boarder.bind(
            "<FocusOut>", self.on_width_of_right_inner_boarder_changed
        )
        self.width_of_bottom_inner_boarder.bind(
            "<FocusOut>", self.on_width_of_bottom_inner_boarder_changed
        )
        self.colour_of_inner_boarder.bind(
            "<FocusOut>", self.on_colour_of_inner_boarder_changed
        )
        self.number_of_cells_horizontally.bind(
            "<FocusOut>", self.on_number_of_cells_horizontally_changed
        )
        self.number_of_cells_vertically.bind(
            "<FocusOut>", self.on_number_of_cells_vertically_changed
        )

        self.height_of_cell.bind("<FocusOut>", self.on_height_of_cell_changed)
        self.top_padding_of_cell.bind("<FocusOut>", self.on_top_padding_of_cell_changed)

        self.bottom_padding_of_cell.bind(
            "<FocusOut>", self.on_bottom_padding_of_cell_changed
        )
        self.size_of_horizontal_gutter_after_cell.bind(
            "<FocusOut>", self.on_size_of_horizontal_gutter_after_cell_changed
        )

        self.width_of_cell.bind("<FocusOut>", self.on_width_of_cell_changed)
        self.left_padding_of_cell.bind(
            "<FocusOut>", self.on_left_padding_of_cell_changed
        )

        self.right_padding_of_cell.bind(
            "<FocusOut>", self.on_right_padding_of_cell_changed
        )
        self.size_of_vertical_gutter_after_cell.bind(
            "<FocusOut>", self.on_size_of_vertical_gutter_after_cell_changed
        )

        self.colour_of_cell_gutter.bind(
            "<FocusOut>", self.on_colour_of_cell_gutter_changed
        )

        self.colour_of_cell.bind("<FocusOut>", self.on_colour_of_cell_changed)

        self.colour_of_cell_padding.bind(
            "<FocusOut>", self.on_colour_of_cell_padding_changed
        )

        self.cell_light_colour.bind("<FocusOut>", self.on_cell_light_colour_changed)

        self.cell_dark_colour.bind("<FocusOut>", self.on_cell_dark_colour_changed)

        self.board_decorator_x_pos.bind(
            "<FocusOut>", self.on_board_decorator_x_pos_changed
        )

        self.board_decorator_y_pos.bind(
            "<FocusOut>", self.on_board_decorator_y_pos_changed
        )

        self.token_name.bind("<FocusOut>", self.on_token_name_changed)

        #  Connect callbacks  - <Return>

        self.name.bind("<Return>", self.on_name_changed)
        self.version.bind("<Return>", self.on_version_changed)
        self.date.bind("<Return>", self.on_date_changed)
        self.author.bind("<Return>", self.on_author_changed)

        self.width_of_left_outer_boarder.bind(
            "<Return>", self.on_width_of_left_outer_boarder_changed
        )
        self.width_of_top_outer_boarder.bind(
            "<Return>", self.on_width_of_top_outer_boarder_changed
        )
        self.width_of_right_outer_boarder.bind(
            "<Return>", self.on_width_of_right_outer_boarder_changed
        )
        self.width_of_bottom_outer_boarder.bind(
            "<Return>", self.on_width_of_bottom_outer_boarder_changed
        )
        self.colour_of_outer_boarder.bind(
            "<Return>", self.on_colour_of_outer_boarder_changed
        )

        self.width_of_left_inner_boarder.bind(
            "<Return>", self.on_width_of_left_inner_boarder_changed
        )
        self.width_of_top_inner_boarder.bind(
            "<Return>", self.on_width_of_top_inner_boarder_changed
        )
        self.width_of_right_inner_boarder.bind(
            "<Return>", self.on_width_of_right_inner_boarder_changed
        )
        self.width_of_bottom_inner_boarder.bind(
            "<Return>", self.on_width_of_bottom_inner_boarder_changed
        )
        self.colour_of_inner_boarder.bind(
            "<Return>", self.on_colour_of_inner_boarder_changed
        )
        self.number_of_cells_horizontally.bind(
            "<Return>", self.on_number_of_cells_horizontally_changed
        )
        self.number_of_cells_vertically.bind(
            "<Return>", self.on_number_of_cells_vertically_changed
        )

        self.height_of_cell.bind("<Return>", self.on_height_of_cell_changed)
        self.top_padding_of_cell.bind("<Return>", self.on_top_padding_of_cell_changed)

        self.bottom_padding_of_cell.bind(
            "<Return>", self.on_bottom_padding_of_cell_changed
        )
        self.size_of_horizontal_gutter_after_cell.bind(
            "<Return>", self.on_size_of_horizontal_gutter_after_cell_changed
        )

        self.width_of_cell.bind("<Return>", self.on_width_of_cell_changed)
        self.left_padding_of_cell.bind("<Return>", self.on_left_padding_of_cell_changed)

        self.right_padding_of_cell.bind(
            "<Return>", self.on_right_padding_of_cell_changed
        )
        self.size_of_vertical_gutter_after_cell.bind(
            "<Return>", self.on_size_of_vertical_gutter_after_cell_changed
        )

        self.colour_of_cell_gutter.bind(
            "<Return>", self.on_colour_of_cell_gutter_changed
        )

        self.colour_of_cell.bind("<Return>", self.on_colour_of_cell_changed)

        self.colour_of_cell_padding.bind(
            "<Return>", self.on_colour_of_cell_padding_changed
        )

        self.cell_light_colour.bind("<Return>", self.on_cell_light_colour_changed)

        self.cell_dark_colour.bind("<Return>", self.on_cell_dark_colour_changed)

        self.board_decorator_x_pos.bind(
            "<Return>", self.on_board_decorator_x_pos_changed
        )

        self.board_decorator_y_pos.bind(
            "<Return>", self.on_board_decorator_y_pos_changed
        )

        self.token_name.bind("<Return>", self.on_token_name_changed)

    def connect_all_accelerators(self) -> None:

        #  Connect menu accelerators.

        self.mainwindow.bind_all("<Control-n>", self.on_new)
        self.mainwindow.bind_all("<Control-o>", self.on_open)
        self.mainwindow.bind_all("<Control-s>", self.on_save)
        self.mainwindow.bind_all("<Control-q>", self.on_quit)

    def initialise_recent_files_list(self) -> None:

        self.recent_files_list: list[str] = []
        self.recent_files: RecentFiles = RecentFiles(
            self.recent_files_list, self.recent_files_menu, self.on_open_recent
        )
        self.recent_files.load_recent_files()

    def run(self) -> None:

        self.load_gameboard()
        self.show_gameboard()
        self.mainwindow.mainloop()

    def load_gameboard(self) -> None:

        self.var_name.set(self.gameboard.name)
        self.var_version.set(self.gameboard.version)
        self.var_date.set(self.gameboard.date)
        self.var_author.set(self.gameboard.author)

        self.var_width_of_left_outer_boarder.set(
            self.gameboard.width_of_left_outer_boarder
        )
        self.var_width_of_top_outer_boarder.set(
            self.gameboard.width_of_top_outer_boarder
        )
        self.var_width_of_right_outer_boarder.set(
            self.gameboard.width_of_right_outer_boarder
        )
        self.var_width_of_bottom_outer_boarder.set(
            self.gameboard.width_of_bottom_outer_boarder
        )
        self.var_colour_of_outer_boarder.set(self.gameboard.colour_of_outer_boarder)
        self.var_width_of_left_inner_boarder.set(
            self.gameboard.width_of_left_inner_boarder
        )
        self.var_width_of_top_inner_boarder.set(
            self.gameboard.width_of_top_inner_boarder
        )
        self.var_width_of_right_inner_boarder.set(
            self.gameboard.width_of_right_inner_boarder
        )
        self.var_width_of_bottom_inner_boarder.set(
            self.gameboard.width_of_bottom_inner_boarder
        )
        self.var_colour_of_inner_boarder.set(self.gameboard.colour_of_inner_boarder)

        self.var_number_of_cells_horizontally.set(
            self.gameboard.number_of_cells_horizontally
        )
        self.var_number_of_cells_vertically.set(
            self.gameboard.number_of_cells_vertically
        )

        self.var_cells_on_rows_row.set(0)
        self.var_height_of_cell.set(self.gameboard.height_of_cell[0])
        self.var_top_padding_of_cell.set(self.gameboard.top_padding_of_cell[0])
        self.var_bottom_padding_of_cell.set(self.gameboard.bottom_padding_of_cell[0])
        self.var_size_of_horizontal_gutter_after_cell.set(
            self.gameboard.size_of_horizontal_gutter_after_cell[0]
        )

        self.var_cells_on_columns_column.set(0)
        self.var_width_of_cell.set(self.gameboard.width_of_cell[0])
        self.var_left_padding_of_cell.set(self.gameboard.left_padding_of_cell[0])
        self.var_right_padding_of_cell.set(self.gameboard.right_padding_of_cell[0])
        self.var_size_of_vertical_gutter_after_cell.set(
            self.gameboard.size_of_vertical_gutter_after_cell[0]
        )

        self.var_colour_of_cell_gutter.set(self.gameboard.colour_of_cell_gutter)

        self.var_cells_on_rows_columns_row.set(0)
        self.var_cells_on_rows_columns_column.set(0)
        self.var_colour_of_cell.set(self.gameboard.colour_of_cell[0][0])
        self.var_colour_of_cell_padding.set(self.gameboard.colour_of_cell_padding[0][0])

        self.var_cell_decorators_row.set(0)
        self.var_cell_decorators_column.set(0)
        self.var_cell_decorator.set(self.gameboard.cell_decorator[0][0])

        if self.gameboard.cell_decorator[0][0] == "":
            self.remove_cell_decorator.configure(state="disabled")
        else:
            self.remove_cell_decorator.configure(state="normal")

        self.var_board_decorator_choice.set("Add decorator")
        self.var_token_choice.set("Add token")

        self.var_placed_tokens_row.set(0)
        self.var_placed_tokens_column.set(0)
        self.var_placed_token_name_choice.set(self.gameboard.placed_tokens[0][0])

        self.gameboard.cell_selected_callback = self.cell_selected

    def show_gameboard(self) -> None:

        self.mainwindow.title(f"Gameboard Designer - {self.gameboard.name}")

        for widget in self.main.winfo_children():
            widget.destroy()

        self.load_decorators()
        self.load_tokens()

        canvas: Canvas = self.gameboard.draw(self.main)
        canvas.pack(anchor=CENTER, expand=True)

    def load_decorators(self) -> None:
        _decorators = [
            f"Decorator {i+1}" for i in range(len(self.gameboard.board_decorator))
        ]
        self.board_decorator_choice.configure(values=["Add decorator"] + _decorators)

        _index = self.board_decorator_choice._values.index(
            self.var_board_decorator_choice.get()
        )

        if _index > 0:
            self.var_board_decorator.set(self.gameboard.board_decorator[_index - 1][0])
            self.var_board_decorator_x_pos.set(
                self.gameboard.board_decorator[_index - 1][1]
            )
            self.var_board_decorator_y_pos.set(
                self.gameboard.board_decorator[_index - 1][2]
            )
        else:
            self.var_board_decorator.set("")
            self.var_board_decorator_x_pos.set(0)
            self.var_board_decorator_y_pos.set(0)

    def load_tokens(self) -> None:
        _tokens = [_token[0] for _token in self.gameboard.tokens]
        self.token_choice.configure(values=["Add token"] + _tokens)

        _index = self.token_choice._values.index(self.var_token_choice.get())

        if _index > 0:
            self.var_token_name.set(self.gameboard.tokens[_index - 1][0])
            self.var_token.set(self.gameboard.tokens[_index - 1][1])
            self.token_name.configure(state="normal")
            self.pick_token.configure(state="normal")
            self.remove_token.configure(state="normal")
        else:
            self.var_token_name.set("")
            self.var_token.set("")
            self.token_name.configure(state="disabled")
            self.pick_token.configure(state="disabled")
            self.remove_token.configure(state="disabled")

        _available_tokens = [_token[0] for _token in self.gameboard.tokens]
        self.placed_token_name_choice.configure(values=_available_tokens)

        if self.placed_token_name_choice.get() == "":
            self.remove_placed_token.configure("disabled")

    #  File menu actions.

    def check_save(self, *args) -> None:
        if self.gameboard.saved is False:
            msg = CTkMessagebox(
                title="Save gameboard",
                message="Do you want to save the current gameboard before continuing?",
                icon="question",
                option_1="No",
                option_2="Yes",
            )
            response = msg.get()

            if response == "Yes":
                self.save()

    def on_new(self, *args) -> None:

        self.check_save()
        self.gameboard = Gameboard()
        self.filename = ""
        self.load_gameboard()
        self.show_gameboard()
        self.palette.set("Details")

    def on_open(self, *args) -> None:

        self.check_save()
        _result = self.open()
        if _result is not None:
            self.gameboard = _result[0]
            self.filename = _result[1]
            self.load_gameboard()
            self.show_gameboard()
            self.palette.set("Details")

    def on_open_recent(self, filename: str) -> None:

        self.check_save()
        _result = self.open_filename(filename)
        if _result is not None:
            self.gameboard = _result[0]
            self.filename = _result[1]
            self.load_gameboard()
            self.show_gameboard()
            self.palette.set("Details")

    def on_clear_recent_files(self) -> None:
        self.recent_files.clear_recent_files_list()

    def on_save(self, *args) -> None:
        self.save()

    def on_save_as(self) -> None:
        self.save_as()

    def on_quit(self, *args) -> None:
        self.check_save()
        self.mainwindow.quit()

    #  File IO

    def open_filename(self, filename: str) -> tuple[Gameboard, str] | None:

        if filename != "":
            _gameboard, _message = Gameboard.load(filename)
            if _gameboard is not None:
                self.recent_files.add_to_recent_files_list(self.relative_path(filename))
                return _gameboard, filename
            else:
                CTkMessagebox(
                    title="Error while loading gameboard",
                    message=_message,
                    icon="cancel",
                )
                return None
        else:
            return None

    def open(self) -> tuple[Gameboard, str] | None:

        _filetypes = (("gameboards", "*.tab"), ("All files", "*.*"))

        _filename: str = filedialog.askopenfilename(
            title="Open gameboard", initialdir=".", filetypes=_filetypes
        )

        return self.open_filename(_filename)

    def save(self):
        if self.filename == "":
            self.save_as()
        else:
            _error = self.gameboard.save(self.filename)
            if _error == "":
                self.recent_files.add_to_recent_files_list(
                    self.relative_path(self.filename)
                )
            else:
                CTkMessagebox(
                    title="Error while saving gameboard", message=_error, icon="cancel"
                )

    def save_as(self):
        _filetypes = (("gameboards", "*.tab"), ("All files", "*.*"))

        _filename: str = filedialog.asksaveasfilename(
            title="Save gameboard", initialdir=".", filetypes=_filetypes
        )
        if _filename != "":
            if not _filename.lower().endswith(".tab"):
                _filename += ".tab"

            _error = self.gameboard.save(_filename)
            if _error == "":
                self.recent_files.add_to_recent_files_list(
                    self.relative_path(_filename)
                )
                self.filename = _filename
            else:
                CTkMessagebox(
                    title="Error while saving gameboard", message=_error, icon="cancel"
                )

    #  Field change callbacks.

    def palette_selected(self, *args):
        if self.palette.get() == "Details":
            self.name.focus()
        if self.palette.get() == "Boarders":
            self.width_of_left_outer_boarder.focus()
        if self.palette.get() == "Cells":
            self.number_of_cells_horizontally.focus()
        if self.palette.get() == "Decorators":
            ...

    def on_name_changed(self, *args) -> None:
        self.gameboard.name = self.var_name.get()
        self.show_gameboard()

    def on_version_changed(self, *args) -> None:
        self.gameboard.version = self.var_version.get()
        self.show_gameboard()

    def on_date_changed(self, *args) -> None:
        self.gameboard.date = self.var_date.get()
        self.show_gameboard()

    def on_author_changed(self, *args) -> None:
        self.gameboard.author = self.var_author.get()
        self.show_gameboard()

    def on_width_of_left_outer_boarder_changed(self, *args) -> None:
        self.gameboard.width_of_left_outer_boarder = validated_int(
            self.var_width_of_left_outer_boarder,
            self.width_of_left_outer_boarder,
            self.gameboard.width_of_left_outer_boarder,
            max=500,
        )
        self.show_gameboard()

    def on_width_of_top_outer_boarder_changed(self, *args) -> None:
        self.gameboard.width_of_top_outer_boarder = validated_int(
            self.var_width_of_top_outer_boarder,
            self.width_of_top_outer_boarder,
            self.gameboard.width_of_top_outer_boarder,
            max=500,
        )
        self.show_gameboard()

    def on_width_of_right_outer_boarder_changed(self, *args) -> None:

        self.gameboard.width_of_right_outer_boarder = validated_int(
            self.var_width_of_right_outer_boarder,
            self.width_of_right_outer_boarder,
            self.gameboard.width_of_right_outer_boarder,
            max=500,
        )
        self.show_gameboard()

    def on_width_of_bottom_outer_boarder_changed(self, *args) -> None:
        self.gameboard.width_of_bottom_outer_boarder = validated_int(
            self.var_width_of_bottom_outer_boarder,
            self.width_of_bottom_outer_boarder,
            self.gameboard.width_of_bottom_outer_boarder,
            max=500,
        )
        self.show_gameboard()

    def on_colour_of_outer_boarder_changed(self, *args) -> None:
        self.gameboard.colour_of_outer_boarder = validated_colour(
            self.var_colour_of_outer_boarder,
            self.colour_of_outer_boarder,
            self.gameboard.colour_of_outer_boarder,
        )
        self.show_gameboard()

    def on_width_of_left_inner_boarder_changed(self, *args) -> None:
        self.gameboard.width_of_left_inner_boarder = validated_int(
            self.var_width_of_left_inner_boarder,
            self.width_of_left_inner_boarder,
            self.gameboard.width_of_left_inner_boarder,
            max=500,
        )
        self.show_gameboard()

    def on_width_of_top_inner_boarder_changed(self, *args) -> None:
        self.gameboard.width_of_top_inner_boarder = validated_int(
            self.var_width_of_top_inner_boarder,
            self.width_of_top_inner_boarder,
            self.gameboard.width_of_top_inner_boarder,
            max=500,
        )
        self.show_gameboard()

    def on_width_of_right_inner_boarder_changed(self, *args) -> None:

        self.gameboard.width_of_right_inner_boarder = validated_int(
            self.var_width_of_right_inner_boarder,
            self.width_of_right_inner_boarder,
            self.gameboard.width_of_right_inner_boarder,
            max=500,
        )
        self.show_gameboard()

    def on_width_of_bottom_inner_boarder_changed(self, *args) -> None:
        self.gameboard.width_of_bottom_inner_boarder = validated_int(
            self.var_width_of_bottom_inner_boarder,
            self.width_of_bottom_inner_boarder,
            self.gameboard.width_of_bottom_inner_boarder,
            max=500,
        )
        self.show_gameboard()

    def on_colour_of_inner_boarder_changed(self, *args) -> None:
        self.gameboard.colour_of_inner_boarder = validated_colour(
            self.var_colour_of_inner_boarder,
            self.colour_of_inner_boarder,
            self.gameboard.colour_of_inner_boarder,
        )
        self.show_gameboard()

    def on_number_of_cells_horizontally_changed(self, *args) -> None:
        _original_number_of_cells: int = self.gameboard.number_of_cells_horizontally
        self.gameboard.number_of_cells_horizontally = validated_int(
            self.var_number_of_cells_horizontally,
            self.number_of_cells_horizontally,
            self.gameboard.number_of_cells_horizontally,
            min=1,
        )

        #  If the number of horizontal cells has reduced then trim the lists that hold multiple values based on the number of columns.

        if self.gameboard.number_of_cells_horizontally < _original_number_of_cells:
            self.gameboard.width_of_cell = self.gameboard.width_of_cell[
                : self.gameboard.number_of_cells_horizontally
            ]
            self.gameboard.left_padding_of_cell = self.gameboard.left_padding_of_cell[
                : self.gameboard.number_of_cells_horizontally
            ]
            self.gameboard.right_padding_of_cell = self.gameboard.right_padding_of_cell[
                : self.gameboard.number_of_cells_horizontally
            ]
            self.gameboard.size_of_vertical_gutter_after_cell = (
                self.gameboard.size_of_vertical_gutter_after_cell[
                    : self.gameboard.number_of_cells_horizontally
                ]
            )

            for _row in range(self.gameboard.number_of_cells_vertically):
                self.gameboard.colour_of_cell[_row] = self.gameboard.colour_of_cell[
                    _row
                ][: self.gameboard.number_of_cells_horizontally]
                self.gameboard.colour_of_cell_padding[_row] = (
                    self.gameboard.colour_of_cell_padding[_row][
                        : self.gameboard.number_of_cells_horizontally
                    ]
                )
                self.gameboard.cell_decorator[_row] = self.gameboard.cell_decorator[
                    _row
                ][: self.gameboard.number_of_cells_horizontally]
                self.gameboard.placed_tokens[_row] = self.gameboard.placed_tokens[_row][
                    : self.gameboard.number_of_cells_horizontally
                ]

        #  If the number of horizontal cells has increased then expand the lists that hold multiple values based on the number of columns.

        if self.gameboard.number_of_cells_horizontally > _original_number_of_cells:
            _increase: int = (
                self.gameboard.number_of_cells_horizontally - _original_number_of_cells
            )

            for _ in range(_increase):

                self.gameboard.width_of_cell.append(
                    self.gameboard.width_of_cell[_original_number_of_cells - 1]
                )
                self.gameboard.left_padding_of_cell.append(
                    self.gameboard.left_padding_of_cell[_original_number_of_cells - 1]
                )
                self.gameboard.right_padding_of_cell.append(
                    self.gameboard.right_padding_of_cell[_original_number_of_cells - 1]
                )
                self.gameboard.size_of_vertical_gutter_after_cell.append(
                    self.gameboard.size_of_vertical_gutter_after_cell[
                        _original_number_of_cells - 1
                    ]
                )

            for _row in range(self.gameboard.number_of_cells_vertically):

                for _ in range(_increase):
                    self.gameboard.colour_of_cell[_row].append(
                        self.gameboard.colour_of_cell[_row][
                            _original_number_of_cells - 1
                        ]
                    )
                    self.gameboard.colour_of_cell_padding[_row].append(
                        self.gameboard.colour_of_cell_padding[_row][
                            _original_number_of_cells - 1
                        ]
                    )
                    self.gameboard.cell_decorator[_row].append("")
                    self.gameboard.placed_tokens[_row].append("")

        self.show_gameboard()

    def on_number_of_cells_vertically_changed(self, *args) -> None:
        _original_number_of_cells: int = self.gameboard.number_of_cells_vertically
        self.gameboard.number_of_cells_vertically = validated_int(
            self.var_number_of_cells_vertically,
            self.number_of_cells_vertically,
            self.gameboard.number_of_cells_vertically,
            min=1,
        )

        #  If the number of vertical cells has reduced then trim the lists that hold multiple values based on the number of rows.

        if self.gameboard.number_of_cells_vertically < _original_number_of_cells:
            self.gameboard.height_of_cell = self.gameboard.height_of_cell[
                : self.gameboard.number_of_cells_vertically
            ]
            self.gameboard.top_padding_of_cell = self.gameboard.top_padding_of_cell[
                : self.gameboard.number_of_cells_vertically
            ]
            self.gameboard.bottom_padding_of_cell = (
                self.gameboard.bottom_padding_of_cell[
                    : self.gameboard.number_of_cells_vertically
                ]
            )
            self.gameboard.size_of_horizontal_gutter_after_cell = (
                self.gameboard.size_of_horizontal_gutter_after_cell[
                    : self.gameboard.number_of_cells_vertically
                ]
            )
            self.gameboard.colour_of_cell = self.gameboard.colour_of_cell[
                : self.gameboard.number_of_cells_vertically
            ]
            self.gameboard.colour_of_cell_padding = (
                self.gameboard.colour_of_cell_padding[
                    : self.gameboard.number_of_cells_vertically
                ]
            )
            self.gameboard.cell_decorator = self.gameboard.cell_decorator[
                : self.gameboard.number_of_cells_vertically
            ]
            self.gameboard.placed_tokens = self.gameboard.placed_tokens[
                : self.gameboard.number_of_cells_vertically
            ]

        #  If the number of vertical cells has increased then expand the lists that hold multiple values based on the number of rows.

        if self.gameboard.number_of_cells_vertically > _original_number_of_cells:
            _increase: int = (
                self.gameboard.number_of_cells_vertically - _original_number_of_cells
            )

            for _ in range(_increase):

                self.gameboard.height_of_cell.append(
                    self.gameboard.height_of_cell[_original_number_of_cells - 1]
                )
                self.gameboard.top_padding_of_cell.append(
                    self.gameboard.top_padding_of_cell[_original_number_of_cells - 1]
                )
                self.gameboard.bottom_padding_of_cell.append(
                    self.gameboard.bottom_padding_of_cell[_original_number_of_cells - 1]
                )
                self.gameboard.size_of_horizontal_gutter_after_cell.append(
                    self.gameboard.size_of_horizontal_gutter_after_cell[
                        _original_number_of_cells - 1
                    ]
                )

                self.gameboard.colour_of_cell.append(
                    self.gameboard.colour_of_cell[_original_number_of_cells - 1].copy()
                )
                self.gameboard.colour_of_cell_padding.append(
                    self.gameboard.colour_of_cell_padding[
                        _original_number_of_cells - 1
                    ].copy()
                )
                self.gameboard.cell_decorator.append(
                    [""] * self.gameboard.number_of_cells_horizontally
                )
                self.gameboard.placed_tokens.append(
                    [""] * self.gameboard.number_of_cells_horizontally
                )

        self.show_gameboard()

    def on_height_of_cell_changed(self, *args) -> None:
        self.gameboard.height_of_cell[int(self.var_cells_on_rows_row.get())] = (
            validated_int(
                self.var_height_of_cell,
                self.height_of_cell,
                self.gameboard.height_of_cell[int(self.var_cells_on_rows_row.get())],
                min=10,
                max=500,
            )
        )
        self.show_gameboard()

    def on_top_padding_of_cell_changed(self, *args) -> None:
        self.gameboard.top_padding_of_cell[int(self.var_cells_on_rows_row.get())] = (
            validated_int(
                self.var_top_padding_of_cell,
                self.top_padding_of_cell,
                self.gameboard.top_padding_of_cell[
                    int(self.var_cells_on_rows_row.get())
                ],
                max=500,
            )
        )
        self.show_gameboard()

    def on_bottom_padding_of_cell_changed(self, *args) -> None:
        self.gameboard.bottom_padding_of_cell[int(self.var_cells_on_rows_row.get())] = (
            validated_int(
                self.var_bottom_padding_of_cell,
                self.bottom_padding_of_cell,
                self.gameboard.bottom_padding_of_cell[
                    int(self.var_cells_on_rows_row.get())
                ],
                max=500,
            )
        )
        self.show_gameboard()

    def on_size_of_horizontal_gutter_after_cell_changed(self, *args) -> None:
        self.gameboard.size_of_horizontal_gutter_after_cell[
            int(self.var_cells_on_rows_row.get())
        ] = validated_int(
            self.var_size_of_horizontal_gutter_after_cell,
            self.size_of_horizontal_gutter_after_cell,
            self.gameboard.size_of_horizontal_gutter_after_cell[
                int(self.var_cells_on_rows_row.get())
            ],
            max=500,
        )
        self.show_gameboard()

    def on_width_of_cell_changed(self, *args) -> None:
        self.gameboard.width_of_cell[int(self.var_cells_on_columns_column.get())] = (
            validated_int(
                self.var_width_of_cell,
                self.width_of_cell,
                self.gameboard.width_of_cell[
                    int(self.var_cells_on_columns_column.get())
                ],
                min=10,
                max=500,
            )
        )
        self.show_gameboard()

    def on_left_padding_of_cell_changed(self, *args) -> None:
        self.gameboard.left_padding_of_cell[
            int(self.var_cells_on_rows_columns_column.get())
        ] = validated_int(
            self.var_left_padding_of_cell,
            self.left_padding_of_cell,
            self.gameboard.left_padding_of_cell[
                int(self.var_cells_on_rows_columns_column.get())
            ],
            max=500,
        )
        self.show_gameboard()

    def on_right_padding_of_cell_changed(self, *args) -> None:
        self.gameboard.right_padding_of_cell[
            int(self.var_cells_on_rows_columns_column.get())
        ] = validated_int(
            self.var_right_padding_of_cell,
            self.right_padding_of_cell,
            self.gameboard.right_padding_of_cell[
                int(self.var_cells_on_rows_columns_column.get())
            ],
            max=500,
        )
        self.show_gameboard()

    def on_size_of_vertical_gutter_after_cell_changed(self, *args) -> None:
        self.gameboard.size_of_vertical_gutter_after_cell[
            int(self.var_cells_on_rows_row.get())
        ] = validated_int(
            self.var_size_of_vertical_gutter_after_cell,
            self.size_of_vertical_gutter_after_cell,
            self.gameboard.size_of_vertical_gutter_after_cell[
                int(self.var_cells_on_rows_row.get())
            ],
            max=500,
        )
        self.show_gameboard()

    def on_colour_of_cell_gutter_changed(self, *args) -> None:
        self.gameboard.colour_of_cell_gutter = validated_colour(
            self.var_colour_of_cell_gutter,
            self.colour_of_cell_gutter,
            self.gameboard.colour_of_cell_gutter,
        )
        self.show_gameboard()

    def on_colour_of_cell_changed(self, *args) -> None:
        self.gameboard.colour_of_cell[int(self.var_cells_on_rows_columns_row.get())][
            int(self.var_cells_on_rows_columns_column.get())
        ] = validated_colour(
            self.var_colour_of_cell,
            self.colour_of_cell,
            self.gameboard.colour_of_cell[
                int(self.var_cells_on_rows_columns_row.get())
            ][int(self.var_cells_on_rows_columns_column.get())],
        )
        self.show_gameboard()

    def on_colour_of_cell_padding_changed(self, *args) -> None:
        self.gameboard.colour_of_cell_padding[
            int(self.var_cells_on_rows_columns_row.get())
        ][int(self.var_cells_on_rows_columns_column.get())] = validated_colour(
            self.var_colour_of_cell_padding,
            self.colour_of_cell_padding,
            self.gameboard.colour_of_cell_padding[
                int(self.var_cells_on_rows_columns_row.get())
            ][int(self.var_cells_on_rows_columns_column.get())],
        )
        self.show_gameboard()

    def on_cell_light_colour_changed(self, *args) -> None:
        self.var_cell_light_colour.set(
            validated_colour(
                self.var_cell_light_colour,
                self.cell_light_colour,
                "#FFFFFF",
            )
        )

    def on_cell_dark_colour_changed(self, *args) -> None:
        self.var_cell_dark_colour.set(
            validated_colour(
                self.var_cell_dark_colour,
                self.cell_dark_colour,
                "#000000",
            )
        )

    def on_board_decorator_x_pos_changed(self, *args) -> None:

        _index = (
            self.board_decorator_choice._values.index(
                self.var_board_decorator_choice.get()
            )
            - 1
        )

        self.gameboard.board_decorator[_index] = (
            self.gameboard.board_decorator[_index][0],
            validated_int(
                self.var_board_decorator_x_pos,
                self.board_decorator_x_pos,
                self.gameboard.board_decorator[_index][1],
                min=0,
                max=1000,
            ),
            self.gameboard.board_decorator[_index][2],
        )
        self.show_gameboard()

    def on_board_decorator_y_pos_changed(self, *args) -> None:
        _index = (
            self.board_decorator_choice._values.index(
                self.var_board_decorator_choice.get()
            )
            - 1
        )

        self.gameboard.board_decorator[_index] = (
            self.gameboard.board_decorator[_index][0],
            self.gameboard.board_decorator[_index][1],
            validated_int(
                self.var_board_decorator_y_pos,
                self.board_decorator_y_pos,
                self.gameboard.board_decorator[_index][2],
                min=0,
                max=1000,
            ),
        )
        self.show_gameboard()

    def on_token_name_changed(self, *args) -> None:

        _index = self.token_choice._values.index(self.token_choice.get()) - 1

        self.gameboard.tokens[_index] = (self.var_token_name.get(), self.token.get())

        _tokens = [_token[0] for _token in self.gameboard.tokens]
        self.token_choice.configure(values=["Add token"] + _tokens)
        self.token_choice.set(self.var_token_name.get())
        self.show_gameboard()

    #  Handle button presses.

    def on_all_outer_width(self):

        self.gameboard.width_of_left_outer_boarder = int(
            self.var_width_of_left_outer_boarder.get()
        )

        self.var_width_of_top_outer_boarder.set(
            self.var_width_of_left_outer_boarder.get()
        )
        self.gameboard.width_of_top_outer_boarder = int(
            self.var_width_of_left_outer_boarder.get()
        )

        self.var_width_of_right_outer_boarder.set(
            self.var_width_of_left_outer_boarder.get()
        )
        self.gameboard.width_of_right_outer_boarder = int(
            self.var_width_of_left_outer_boarder.get()
        )

        self.var_width_of_bottom_outer_boarder.set(
            self.var_width_of_left_outer_boarder.get()
        )
        self.gameboard.width_of_bottom_outer_boarder = int(
            self.var_width_of_left_outer_boarder.get()
        )
        self.show_gameboard()

    def on_all_inner_width(self):

        self.gameboard.width_of_left_inner_boarder = int(
            self.var_width_of_left_inner_boarder.get()
        )

        self.var_width_of_top_inner_boarder.set(
            self.var_width_of_left_inner_boarder.get()
        )
        self.gameboard.width_of_top_inner_boarder = int(
            self.var_width_of_left_inner_boarder.get()
        )

        self.var_width_of_right_inner_boarder.set(
            self.var_width_of_left_inner_boarder.get()
        )
        self.gameboard.width_of_right_inner_boarder = int(
            self.var_width_of_left_inner_boarder.get()
        )

        self.var_width_of_bottom_inner_boarder.set(
            self.var_width_of_left_inner_boarder.get()
        )
        self.gameboard.width_of_bottom_inner_boarder = int(
            self.var_width_of_left_inner_boarder.get()
        )
        self.show_gameboard()

    def on_all_rows_height(self):
        self.gameboard.height_of_cell = [
            int(self.var_height_of_cell.get())
        ] * self.gameboard.number_of_cells_vertically
        self.show_gameboard()

    def on_all_rows_top(self):
        self.gameboard.top_padding_of_cell = [
            int(self.var_top_padding_of_cell.get())
        ] * self.gameboard.number_of_cells_vertically
        self.show_gameboard()

    def on_all_rows_bottom(self):
        self.gameboard.bottom_padding_of_cell = [
            int(self.var_bottom_padding_of_cell.get())
        ] * self.gameboard.number_of_cells_vertically
        self.show_gameboard()

    def on_all_rows_horizontal_gutter(self):
        self.gameboard.size_of_horizontal_gutter_after_cell = [
            int(self.var_size_of_horizontal_gutter_after_cell.get())
        ] * self.gameboard.number_of_cells_vertically
        self.show_gameboard()

    def on_all_columns_width(self):
        self.gameboard.width_of_cell = [
            int(self.var_width_of_cell.get())
        ] * self.gameboard.number_of_cells_horizontally
        self.show_gameboard()

    def on_all_columns_left(self):
        self.gameboard.left_padding_of_cell = [
            int(self.var_left_padding_of_cell.get())
        ] * self.gameboard.number_of_cells_horizontally
        self.show_gameboard()

    def on_all_columns_right(self):
        self.gameboard.right_padding_of_cell = [
            int(self.var_right_padding_of_cell.get())
        ] * self.gameboard.number_of_cells_horizontally
        self.show_gameboard()

    def on_all_columns_vertical_gutter(self):
        self.gameboard.size_of_vertical_gutter_after_cell = [
            int(self.var_size_of_vertical_gutter_after_cell.get())
        ] * self.gameboard.number_of_cells_horizontally
        self.show_gameboard()

    def on_all_cell_colour(self):
        for _row in range(self.gameboard.number_of_cells_vertically):
            for _column in range(self.gameboard.number_of_cells_horizontally):
                self.gameboard.colour_of_cell[_row][
                    _column
                ] = self.var_colour_of_cell.get()
        self.show_gameboard()

    def on_all_cells_padding_colour(self):
        for _row in range(self.gameboard.number_of_cells_vertically):
            for _column in range(self.gameboard.number_of_cells_horizontally):
                self.gameboard.colour_of_cell_padding[_row][
                    _column
                ] = self.var_colour_of_cell_padding.get()
        self.show_gameboard()

    def on_apply_checkerboard_colours(self):

        for _row_index in range(self.gameboard.number_of_cells_vertically):
            for _column_index in range(self.gameboard.number_of_cells_horizontally):
                if _row_index % 2 == 0:
                    if _column_index % 2 == 0:
                        self.gameboard.colour_of_cell[_row_index][
                            _column_index
                        ] = self.var_cell_light_colour.get()
                    else:
                        self.gameboard.colour_of_cell[_row_index][
                            _column_index
                        ] = self.var_cell_dark_colour.get()
                else:
                    if _column_index % 2 != 0:
                        self.gameboard.colour_of_cell[_row_index][
                            _column_index
                        ] = self.var_cell_light_colour.get()
                    else:
                        self.gameboard.colour_of_cell[_row_index][
                            _column_index
                        ] = self.var_cell_dark_colour.get()

        self.show_gameboard()

    def on_pick_outer_boarder_colour(self) -> None:
        pick_color: AskColor = AskColor()
        colour: str = pick_color.get()
        if colour is not None:
            self.var_colour_of_outer_boarder.set(colour)
            self.gameboard.colour_of_outer_boarder = (
                self.var_colour_of_outer_boarder.get()
            )
            self.show_gameboard()

    def on_pick_inner_boarder_colour(self) -> None:
        pick_color: AskColor = AskColor()
        colour: str = pick_color.get()
        if colour is not None:
            self.var_colour_of_inner_boarder.set(colour)
            self.gameboard.colour_of_inner_boarder = (
                self.var_colour_of_inner_boarder.get()
            )
            self.show_gameboard()

    def on_pick_gutter_colour(self) -> None:
        pick_color: AskColor = AskColor()
        colour: str = pick_color.get()
        if colour is not None:
            self.var_colour_of_cell_gutter.set(colour)
            self.gameboard.colour_of_cell_gutter = self.var_colour_of_cell_gutter.get()
            self.show_gameboard()

    def on_pick_cell_colour(self) -> None:
        pick_color: AskColor = AskColor()
        colour: str = pick_color.get()
        if colour is not None:
            self.var_colour_of_cell.set(colour)
            self.gameboard.colour_of_cell[
                int(self.var_cells_on_rows_columns_row.get())
            ][
                int(self.var_cells_on_rows_columns_column.get())
            ] = self.var_colour_of_cell.get()
            self.show_gameboard()

    def on_pick_cell_padding_colour(self) -> None:
        pick_color: AskColor = AskColor()
        colour: str = pick_color.get()
        if colour is not None:
            self.var_colour_of_cell_padding.set(colour)
            self.gameboard.colour_of_cell_padding[
                int(self.var_cells_on_rows_columns_row.get())
            ][
                int(self.var_cells_on_rows_columns_column.get())
            ] = self.var_colour_of_cell_padding.get()
            self.show_gameboard()

    def on_pick_cell_light_colour(self) -> None:
        pick_color: AskColor = AskColor()
        colour: str = pick_color.get()
        if colour is not None:
            self.var_cell_light_colour.set(colour)

    def on_pick_cell_dark_colour(self) -> None:
        pick_color: AskColor = AskColor()
        colour: str = pick_color.get()
        if colour is not None:
            self.var_cell_dark_colour.set(colour)

    def on_pick_cell_decorator(self) -> None:
        _filetypes = (("images", "*.png"), ("All files", "*.*"))

        _filename: str = filedialog.askopenfilename(
            title="Select decorator", initialdir=".", filetypes=_filetypes
        )
        if _filename != "":
            self.var_cell_decorator.set(self.relative_path(_filename))
            self.gameboard.cell_decorator[
                int(self.var_cells_on_rows_columns_row.get())
            ][int(self.var_cells_on_rows_columns_column.get())] = self.relative_path(
                _filename
            )

        self.show_gameboard()

    def on_remove_cell_decorator(self) -> None:
        self.gameboard.cell_decorator[int(self.var_cell_decorators_row.get())][
            int(self.var_cell_decorators_column.get())
        ] = ""
        self.var_cell_decorator.set("")
        self.remove_cell_decorator.configure(state="disabled")

        self.show_gameboard()

    def on_board_decorator_selected(self, choice: str) -> None:
        if choice == "Add decorator":
            self.on_add_board_decorator()
        else:
            _index = self.board_decorator_choice._values.index(choice) - 1

            self.var_board_decorator.set(self.gameboard.board_decorator[_index][0])
            self.var_board_decorator_x_pos.set(
                self.gameboard.board_decorator[_index][1]
            )
            self.var_board_decorator_y_pos.set(
                self.gameboard.board_decorator[_index][2]
            )

        self.pick_board_decorator.configure(state="normal")
        self.board_decorator_x_pos.configure(state="normal")
        self.board_decorator_y_pos.configure(state="normal")
        self.remove_board_decorator.configure(state="normal")

    def on_add_board_decorator(self) -> None:
        _index = len(self.board_decorator_choice._values)
        self.board_decorator_choice.configure(
            values=self.board_decorator_choice._values + [f"Decorator {_index}"]
        )
        self.var_board_decorator_choice.set(f"Decorator {_index}")
        self.var_board_decorator.set("")
        self.var_board_decorator_x_pos.set(0)
        self.var_board_decorator_y_pos.set(0)
        self.gameboard.board_decorator.append(("", 0, 0))

        self.pick_board_decorator.configure(state="normal")
        self.board_decorator_x_pos.configure(state="normal")
        self.board_decorator_y_pos.configure(state="normal")
        self.remove_board_decorator.configure(state="normal")

        self.on_pick_board_decorator()

    def on_pick_board_decorator(self) -> None:
        _filetypes = (("images", "*.png"), ("All files", "*.*"))

        _filename: str = filedialog.askopenfilename(
            title="Select decorator", initialdir=".", filetypes=_filetypes
        )
        if _filename != "":
            _index = (
                self.board_decorator_choice._values.index(
                    self.var_board_decorator_choice.get()
                )
                - 1
            )
            self.var_board_decorator.set(self.relative_path(_filename))
            self.gameboard.board_decorator[_index] = (
                self.relative_path(_filename),
                self.var_board_decorator_x_pos.get(),
                self.var_board_decorator_y_pos.get(),
            )

        self.show_gameboard()

    def on_remove_board_decorator(self) -> None:
        _index = (
            self.board_decorator_choice._values.index(
                self.var_board_decorator_choice.get()
            )
            - 1
        )
        del self.board_decorator_choice._values[_index + 1]
        del self.gameboard.board_decorator[_index]
        self.var_board_decorator_choice.set("Add decorator")
        self.var_board_decorator.set("")
        self.var_board_decorator_x_pos.set(0)
        self.var_board_decorator_y_pos.set(0)

        self.pick_board_decorator.configure(state="disabled")
        self.board_decorator_x_pos.configure(state="disabled")
        self.board_decorator_y_pos.configure(state="disabled")
        self.remove_board_decorator.configure(state="disabled")

        self.show_gameboard()

    def on_token_choice(self, choice: str) -> None:

        if choice == "Add token":
            self.on_add_token()
        else:
            _index = self.token_choice._values.index(choice) - 1

            self.var_token_name.set(self.gameboard.tokens[_index][0])
            self.var_token.set(self.gameboard.tokens[_index][1])

        self.token_name.configure(state="normal")
        self.pick_token.configure(state="normal")
        self.remove_token.configure(state="normal")

    def on_add_token(self) -> None:

        self.gameboard.tokens.append(("Token", ""))
        self.load_tokens()

        self.var_token_choice.set(f"Token")
        self.var_token.set("")
        self.var_token_name.set("Token")

        self.token_name.configure(state="normal")
        self.pick_token.configure(state="normal")
        self.remove_token.configure(state="normal")

        self.on_pick_token()

    def on_pick_token(self) -> None:

        _filetypes = (("images", "*.png"), ("All files", "*.*"))

        _filename: str = filedialog.askopenfilename(
            title="Select token", initialdir=".", filetypes=_filetypes
        )
        if _filename != "":
            _index = self.token_choice._values.index(self.var_token_choice.get()) - 1
            self.var_token.set(self.relative_path(_filename))
            self.gameboard.tokens[_index] = (
                self.var_token_name.get(),
                self.relative_path(_filename),
            )

        self.show_gameboard()

    def on_remove_token(self) -> None:

        _token = self.token_choice.get()
        _index = self.token_choice._values.index(_token) - 1
        del self.token_choice._values[_index + 1]
        del self.gameboard.tokens[_index]
        self.var_token_choice.set("Add token")
        self.var_token_name.set("")
        self.var_token.set("")

        self.token_name.configure(state="disabled")
        self.pick_token.configure(state="disabled")
        self.remove_token.configure(state="disabled")

        for _row, _ in enumerate(self.gameboard.placed_tokens):
            for _column, _ in enumerate(self.gameboard.placed_tokens[_row]):
                if self.gameboard.placed_tokens[_row][_column] == _token:
                    self.gameboard.placed_tokens[_row][_column] = ""

        if self.placed_token_name_choice.get() == _token:
            self.placed_token_name_choice.set("")

        self.show_gameboard()

    def on_placed_token_name_choice(self, choice: str) -> None:
        self.gameboard.placed_tokens[int(self.placed_tokens_row.get())][
            int(self.placed_tokens_column.get())
        ] = choice
        self.show_gameboard()

    def on_remove_placed_token(self) -> None:
        self.gameboard.placed_tokens[int(self.var_placed_tokens_row.get())][
            int(self.var_placed_tokens_column.get())
        ] = ""
        self.var_placed_token_name_choice.set("")
        self.remove_placed_token.configure(state="disabled")

        self.show_gameboard()

    #  Handle cell selection.

    def cell_selected(self, cell: tuple[int, int]) -> None:
        _row: int = cell[0]
        _column: int = cell[1]

        if _row == -1 or _column == -1:
            return

        self.var_cells_on_rows_row.set(_row)
        self.var_height_of_cell.set(self.gameboard.height_of_cell[_row])
        self.var_top_padding_of_cell.set(self.gameboard.top_padding_of_cell[_row])
        self.var_bottom_padding_of_cell.set(self.gameboard.bottom_padding_of_cell[_row])
        self.var_size_of_horizontal_gutter_after_cell.set(
            self.gameboard.size_of_horizontal_gutter_after_cell[_row]
        )

        self.var_cells_on_columns_column.set(_column)
        self.var_width_of_cell.set(self.gameboard.width_of_cell[_column])
        self.var_left_padding_of_cell.set(self.gameboard.left_padding_of_cell[_column])
        self.var_right_padding_of_cell.set(
            self.gameboard.right_padding_of_cell[_column]
        )
        self.var_size_of_vertical_gutter_after_cell.set(
            self.gameboard.size_of_vertical_gutter_after_cell[_column]
        )

        self.var_cells_on_rows_columns_row.set(_row)
        self.var_cells_on_rows_columns_column.set(_column)

        self.var_colour_of_cell.set(self.gameboard.colour_of_cell[_row][_column])
        self.var_colour_of_cell_padding.set(
            self.gameboard.colour_of_cell_padding[_row][_column]
        )

        self.var_cell_decorators_row.set(_row)
        self.var_cell_decorators_column.set(_column)
        self.var_cell_decorator.set(self.gameboard.cell_decorator[_row][_column])

        if self.gameboard.cell_decorator[_row][_column] == "":
            self.remove_cell_decorator.configure(state="disabled")
        else:
            self.remove_cell_decorator.configure(state="normal")

        self.var_placed_tokens_row.set(_row)
        self.var_placed_tokens_column.set(_column)
        self.var_placed_token_name_choice.set(
            self.gameboard.placed_tokens[_row][_column]
        )

        if self.placed_token_name_choice.get() == "":
            self.remove_placed_token.configure(state="disabled")
        else:
            self.remove_placed_token.configure(state="normal")

    #  Handle image retreival, resizing and caching.

    def get_image(
        self, filename: str, width: Optional[int], height: Optional[int]
    ) -> Optional[ImageTk.PhotoImage]:
        if filename in self.images:
            return self.images[filename]
        else:
            try:
                _image = Image.open(filename)  # type:ignore

                if width is not None and height is not None:
                    _resized_image = _ctkImage.resize()  # type:ignore
                else:
                    _resized_image = CTkImage(
                        _image,
                        _image,
                    )
                    _resized_image = _image
                _decorator = ImageTk.PhotoImage(_resized_image)
                self.images[filename] = _decorator
                return _decorator
            except Exception:
                return None

    #  Convert absolute to relative path.

    def relative_path(self, target: str) -> str:

        if target.startswith(".\\"):
            return target

        #  Get script launch directory.

        script_path = Path(__file__).resolve()
        launch_directory = script_path.parent

        #  Return path of path of target relative to launch directory.

        _origin = Path(launch_directory)
        _destination = Path(target)

        _relative_path = _destination.relative_to(_origin)

        return ".\\" + str(_relative_path)


def main() -> None:
    app = GameboarddesignerApp()
    app.run()


if __name__ == "__main__":
    main()
