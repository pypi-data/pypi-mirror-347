"""
This example shows how to connect the admin pages to a backend REST api.
"""

from __future__ import annotations

import os
import enum
from typing import Any
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from nicegui import ui

from pyfost.adminui.admin import Admin
from pyfost.adminui.model_base import AdminModel, Field


#
# --- MODELS ---
#
class TaskStatusEnum(str, enum.Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    BLOCKED = "Blocked"


class Task(AdminModel):
    id: int
    task_type: str
    assignee: str | None = None
    notes: str | None = None
    assignment_id: int
    status: TaskStatusEnum


class Seat(AdminModel):
    id: int
    code: str
    floor_id: int
    x_coord: int
    y_coord: int


class Floor(AdminModel):
    id: int
    level: str
    facility_id: int
    seats: list[Seat]

    # @classmethod
    # def render_in_list(cls, model, admin):
    #     # return f"[{model.level}]"
    #     prefix = "/admin"
    #     pk = model.id
    #     model_type_name = model.__class__.__name__

    #     ui.button(
    #         model.display("level", admin),
    #         on_click=lambda p=prefix, m=model_type_name, pk=pk: ui.navigate.to(
    #             f"{p}/{m}/{pk}"
    #         ),
    #     ).props("flat")


class Facility(AdminModel):
    id: int
    name: str
    floors: list[Floor]

    @classmethod
    def cell_floors(cls, model, admin):
        return ", ".join([t.level for t in model.floors])

    @classmethod
    def render_floors(cls, model, admin):
        with ui.row():
            for t in model.floors:
                ui.button(
                    t.level,
                    on_click=lambda t=t: ui.navigate.to(
                        f"{admin.prefix}/{t.__class__.__name__}/{t.id}"
                    ),
                ).props("flat")


#
# --- CLIENT ---
#
class API:
    def __init__(self, api_url: str = "http://127.0.0.1:8000"):
        api_url = os.getenv("API_BASE_URL", api_url)
        api_url = api_url if api_url.endswith("/") else api_url + "/"

        self.current_facility_id = None
        self.current_floor_id = None

        self._client = httpx.AsyncClient(base_url=api_url, timeout=2.0)

    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Helper function to make requests and handle basic errors."""
        try:
            response = await self._client.request(method, endpoint, **kwargs)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            if response.status_code == 204:  # No Content
                return None
            return response.json()
        except httpx.HTTPStatusError as e:
            # Try to get detail from response, otherwise use generic message
            detail = (
                e.response.json().get("detail", e.response.text)
                if e.response
                else str(e)
            )
            print(
                f"HTTP Error: {e.response.status_code} - {detail}"
            )  # Log detailed error
            raise Exception(f"API Error ({e.response.status_code}): {detail}") from e
        except httpx.RequestError as e:
            print(f"Request Error: {e}")
            raise Exception(f"Network or connection error: {e}") from e
        except Exception as e:
            print(f"Unexpected Error during API call: {e}")
            raise Exception(
                "An unexpected error occurred while contacting the API."
            ) from e

    async def get_facilities(self) -> list[Facility]:
        return [Facility(**i) for i in await self._request("GET", "facilities/")]

    async def get_floors_for_facility(self, facility_id: int) -> list[dict[str, Any]]:
        return await self._request("GET", f"facilities/{facility_id}/floors/")

    async def get_floors(self) -> list[Floor]:
        return [
            Floor(**i)
            for i in await self.get_floors_for_facility(self.current_facility_id)
        ]

    async def get_seats_for_floor(self, floor_id: int) -> list[dict[str, Any]]:
        return await self._request("GET", f"floors/{floor_id}/seats/?limit=1000")

    async def get_seats(self) -> list[dict[str, Any]]:
        return [
            Seat(**i) for i in await self.get_seats_for_floor(self.current_floor_id)
        ]


#
# --- APP ---
#
def create_admin():
    api = API()
    admin = Admin("/admin")

    async def get_f() -> list[Facility]:
        return await api.get_facilities()

    async def get_s() -> list[Seat]:
        return await api.get_seats()

    async def get_fl() -> list[Floor]:
        return await api.get_floors()

    admin.add_view(Seat, get_s)
    admin.add_view(Floor, get_fl)
    admin.add_view(Facility, get_f)

    return admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # print(100 * "#")
    yield
    # print(100 * "#")


app = FastAPI(lifespan=lifespan)
admin = create_admin()
admin.add_to(app)
ui.run_with(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "pyfost.adminui.examples.backend_api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
