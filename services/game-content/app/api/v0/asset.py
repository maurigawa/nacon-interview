from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.models.v0.asset import Asset, AssetCreate, AssetPatch, AssetRead
from app.persistence.engine import get_session

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("/", response_model=AssetRead)
def create_asset(asset: AssetCreate, session: Session = Depends(get_session)):
    db_asset = Asset.model_validate(asset)
    session.add(db_asset)
    session.commit()
    session.refresh(db_asset)
    return AssetRead.model_validate(db_asset)


@router.get("/", response_model=list[AssetRead])
def read_assets(
    offset: int = 0,
    limit: int = Query(default=100),
    session: Session = Depends(get_session),
):
    assets = session.exec(select(Asset).offset(offset).limit(limit)).all()
    return [AssetRead.model_validate(asset) for asset in assets]


@router.get("/{asset_id}", response_model=AssetRead)
def read_asset(asset_id: int, session: Session = Depends(get_session)):
    db_asset = session.get(Asset, asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return AssetRead.model_validate(db_asset)


@router.patch("/{asset_id}", response_model=AssetRead)
def update_asset(
    asset_id: int, asset: AssetPatch, session: Session = Depends(get_session)
):
    db_asset = session.get(Asset, asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    asset_data = asset.model_dump(exclude_unset=True)
    for key, value in asset_data.items():
        setattr(db_asset, key, value)
    db_asset.updated_at = datetime.now()

    session.add(db_asset)
    session.commit()
    session.refresh(db_asset)
    return AssetRead.model_validate(db_asset)


@router.delete("/{asset_id}")
def delete_asset(*, session: Session = Depends(get_session), asset_id: int):
    db_asset = session.get(Asset, asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    session.delete(db_asset)
    session.commit()
    return {"ok": True}
