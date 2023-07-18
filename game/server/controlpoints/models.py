from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

import game.theater
from game.server.leaflet import LeafletPoint

if TYPE_CHECKING:
    from game import Game
    from game.theater import ControlPoint
    from game.theater import AircraftType


class ControlPointJs(BaseModel):
    id: UUID
    name: str
    blue: bool
    position: LeafletPoint
    mobile: bool
    destination: LeafletPoint | None
    sidc: str
    active_ammo_depot: int
    active_fuel_depot: int

    class Config:
        title = "ControlPoint"

    @staticmethod
    def for_control_point(control_point: ControlPoint) -> ControlPointJs:
        destination = None
        if control_point.target_position is not None:
            destination = control_point.target_position.latlng()
        return ControlPointJs(
            id=control_point.id,
            name=control_point.name,
            blue=control_point.captured,
            position=control_point.position.latlng(),
            mobile=control_point.moveable and control_point.captured,
            destination=destination,
            sidc=str(control_point.sidc()),
            active_ammo_depot=control_point.active_ammo_depots_count,
            active_fuel_depot=control_point.active_fuel_depots_count,
        )

    @staticmethod
    def all_in_game(game: Game) -> list[ControlPointJs]:
        return [
            ControlPointJs.for_control_point(cp) for cp in game.theater.controlpoints
        ]
