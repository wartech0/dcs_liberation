from fastapi import APIRouter, Depends

from game import Game
from .models import PackageJS
from ..dependencies import GameContext

router: APIRouter = APIRouter(prefix="/packages")


@router.get("/", operation_id="list_blue_packages", response_model=list[PackageJS])
def list_blue_packages(
    game: Game = Depends(GameContext.require),
) -> list[PackageJS]:
    return PackageJS.all_blue_in_game(game)
