#!/usr/bin/python3

#  type: ignore

import re

from CTkMessagebox import CTkMessagebox
from customtkinter import CTkEntry, StringVar

#  Validation.


def validated_int(
    textvariable: StringVar, entry: CTkEntry, data: int, min: int = 0, max: int = 50
) -> int:

    try:
        _data = int(textvariable.get())
        if min <= _data <= max:
            data = _data
        else:
            raise ValueError
    except ValueError:
        textvariable.set(data)
        entry.select_clear()
        entry.focus_set()
        CTkMessagebox(
            title="Value error",
            message=f"Please enter a valid integer between {min} and {max}.",
            icon="cancel",
        )
    finally:
        return data


def validated_colour(textvariable: StringVar, entry: CTkEntry, data: int) -> int:

    hex_color_regex = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    if re.match(hex_color_regex, textvariable.get()):

        return textvariable.get()

    else:
        textvariable.set(data)
        entry.select_clear()
        entry.focus_set()
        CTkMessagebox(
            title="Value error",
            message="Please enter a valid hex colour code.",
            icon="cancel",
        )
        return data
