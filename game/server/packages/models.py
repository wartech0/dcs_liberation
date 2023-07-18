from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import BaseModel


if TYPE_CHECKING:
    from game import Game
    from game.ato import Package, FlightType


class PackageJS(BaseModel):
    id: UUID
    desc: str
    has_players: bool
    departure_time: str
    target_name: str

    class Config:
        title = "Package"

    @staticmethod
    def from_package(package: Package) -> PackageJS:
        return PackageJS(
            id=uuid4(),
            desc=package.package_description,
            has_players=package.has_players,
            departure_time=f"{package.mission_departure_time}",
            target_name=package.target.name,
        )

    @staticmethod
    def all_blue_in_game(game: Game) -> list[PackageJS]:
        packages = []
        for package in game.blue.ato.packages:
            packages.append(PackageJS.from_package(package))

        return packages
