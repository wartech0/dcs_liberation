from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel


if TYPE_CHECKING:
    from game import Game
    from game.ato import Package, FlightType


class PackageJS(BaseModel):
    desc: str
    has_players: bool

    class Config:
        title = "Package"

    @staticmethod
    def from_package(package: Package) -> PackageJS:
        return PackageJS(
            desc=package.package_description,
            has_players=package.has_players,
        )

    @staticmethod
    def all_blue_in_game(game: Game) -> list[PackageJS]:
        packages = []
        for package in game.blue.ato.packages:
            packages.append(PackageJS.from_package(package))

        return packages
