from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel


if TYPE_CHECKING:
    from game import Game
    from game.ato import Package, FlightType


class PackagesJS(BaseModel):
    desc: str
    primary_task: FlightType | None
    has_players: bool
    departure_time: datetime

    @staticmethod
    def all_blue_in_game(game: Game) -> list[PackagesJS]:
        packages = []
        for package in game.blue.ato.packages:
            desc = (package.package_description,)
            primary_task = (package.primary_task,)
            has_players = (package.has_players,)
            departure_time = package.mission_departure_time

        return packages
