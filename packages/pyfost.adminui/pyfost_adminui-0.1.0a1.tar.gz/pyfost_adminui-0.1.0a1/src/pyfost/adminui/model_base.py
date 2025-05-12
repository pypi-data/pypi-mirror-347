from __future__ import annotations

from typing import Callable, TYPE_CHECKING

from pydantic import BaseModel, Field
from nicegui import ui

if TYPE_CHECKING:
    from .admin import Admin
    from .model_view import ModelView


class AdminModel(BaseModel):

    def cell(self, field_name, admin):
        """
        Return the content to use in a table cell for the given field.
        If a method `cell_<field_name>()` is defined on the model, it will
        be used to generate the content by calling it with args: (model, admin)
        """
        try:
            cell = getattr(self, f"cell_{field_name}")
        except AttributeError:
            return str(getattr(self, field_name, f"field not found:{field_name!r}"))
        else:
            return cell(self, admin)

    def display(self, field_name, admin):
        """
        Return a text representation of the value in field_name.
        If a method `display_<field_name>()` is defined on the model, it will
        be used to generate the text by calling it with args: (model, admin)
        """
        try:
            display = getattr(self, f"display_{field_name}")
        except AttributeError:
            return getattr(self, field_name)
        else:
            return display(self, admin)

    def render(self, field_name, admin: Admin):
        """
        Renders the form ui for the given field.
        If a method `render_<field_name>()` is defined on the model, it will
        be used to render the field ui by calling it with args: (model, admin)

        Default is to render a chip with the display value
        """
        try:
            renderer = getattr(self, f"render_{field_name}")
        except AttributeError:
            admin = admin
            prefix = admin.prefix
            model_type_name = self.__class__.__name__
            model_view = admin.get_model_view_for(self)
            pk = getattr(self, model_view.model_pk_name)
            ui.button(
                self.display(field_name, admin),
                on_click=lambda p=prefix, m=model_type_name, pk=pk: ui.navigate.to(
                    f"{p}/{m}/{pk}"
                ),
            ).props("flat")
        else:
            return renderer(self, admin)

    def render_editor(self, field_name, admin: Admin):
        value = repr(getattr(self, field_name))
        with ui.chip(f"{field_name}"):
            ui.tooltip(value)
