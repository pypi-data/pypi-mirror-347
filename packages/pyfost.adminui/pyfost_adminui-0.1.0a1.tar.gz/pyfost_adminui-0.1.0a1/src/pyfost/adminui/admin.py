from enum import Enum

from fastapi import APIRouter, FastAPI
from nicegui import ui

from .model_view import ModelView
from .model_card import model_card

from .renderers.field import get_default_renderers
from .renderers.column import get_default_column_renderers


class Admin:
    def __init__(self, prefix: str = "/admin", tags: list[str | Enum] | None = None):
        print(
            "------------------ NEW ADMIN",
            self,
        )
        self.api_router = APIRouter(
            prefix=prefix,
        )
        self.title = "Admin"
        self._views = {}
        self._column_renderers = get_default_column_renderers()
        self._field_renderers = get_default_renderers()

    @property
    def prefix(self) -> str:
        return self.api_router.prefix

    def add_view(self, ModelType, getter, pk_name: str = "id"):
        view = ModelView(self, ModelType, getter, pk_name)
        self._views[ModelType] = view

    def get_model_view_for(self, model) -> ModelView:
        return self._views[model.__class__]

    def add_to(self, app: FastAPI):
        @ui.page("", api_router=self.api_router)
        def admin() -> None:
            self.render_header()
            self.render_left_drawer()
            self.render_index()

        for ModelType, view in self._views.items():

            @ui.page(f"/{view.model_type_name}", api_router=self.api_router)
            async def model_page(view=view):
                self.render_header()
                self.render_left_drawer()

                @ui.refreshable
                async def main_area():
                    ui.label(f"{view!r} -> {view.model_type.__name__}")
                    await view.render()

                await main_area()

            @ui.page(f"/{view.model_type_name}/{{ID}}", api_router=self.api_router)
            def item_detail(ID, view=view) -> None:
                try:
                    ID = int(ID)
                except ValueError:
                    pass

                self.render_header()
                self.render_left_drawer()

                @ui.refreshable
                def main_area():
                    ui.button("Back", on_click=ui.navigate.back)
                    ui.label(f"{view!r} -> {view.model_type.__name__}")
                    model = view.get_by_pk(ID)
                    if model is None:
                        ui.markdown(
                            "# 😭\n"
                            f"Could not find {view.model_type.__name__} model with primary key {ID!r}.\n\n"
                            f"Available ids are: \n\n - {'\n - '.join(view._by_pk.keys())}"
                        )
                    else:
                        model_card(
                            view.get_by_pk(ID), self, editable=True, with_menu=True
                        )

                main_area()

        app.include_router(self.api_router)

    def render_header(self):
        with ui.header(elevated=True):
            ui.label(self.title)

    def render_left_drawer(self):
        prefix = self.api_router.prefix
        with ui.left_drawer(value=True).classes("bg-stone-600"):
            for view in self._views.values():
                name = view.model_type_name
                ui.button(
                    name, on_click=lambda n=name: ui.navigate.to(f"{prefix}/{n}")
                ).props("flat")

    def render_index(self):
        ui.markdown(f"# ✨ Welcome to {self.prefix} ✨")

    def get_field_renderer(self, model, field, value, editable: bool):
        for field_renderer in self._field_renderers:
            if field_renderer.handles(self, model, field, value, editable):
                return field_renderer.render
        return None

    def get_column_renderer(self, ModelType, column: dict[str, str]):
        for column_renderer in self._column_renderers:
            if column_renderer.handles(self, ModelType, column):
                return column_renderer(self, ModelType, column)
