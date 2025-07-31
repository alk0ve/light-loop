from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

ASSET_FOLDER: Final = Path(__file__).resolve().parent


def asset(name: str) -> Path:
    return ASSET_FOLDER / name
