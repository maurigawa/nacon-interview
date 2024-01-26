from enum import Enum
from typing import Optional

from sqlmodel import Field

from .persistence_base import NSQLModel, PersistenceBase


class AssetType(str, Enum):
    IMAGE = "image"
    SOUND = "sound"
    MUSIC = "music"
    VIDEO = "video"


class AssetBase(NSQLModel):
    name: str = Field(index=True, unique=True)
    latest_version: float
    file_path: str


class AssetCreateRead(NSQLModel):
    type: AssetType


class Asset(AssetBase, AssetCreateRead, PersistenceBase, table=True):
    model_version: float = 0.1


class AssetCreate(AssetBase, AssetCreateRead):
    ...


class AssetPut(AssetBase):
    ...


class AssetPatch(NSQLModel):
    # attributes are redefined because they should
    # be Optionnal for patch endpoint
    name: Optional[str] = Field(index=True, unique=True, default=None)
    latest_version: Optional[float] = None


class AssetRead(AssetBase, AssetCreateRead, PersistenceBase):
    ...
