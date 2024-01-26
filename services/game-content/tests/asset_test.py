from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.v0.asset import Asset, AssetType


def test_create_asset(client: TestClient):
    body = {
        "type": "image",
        "name": "test_img",
        "latest_version": 0.1,
        "file_path": "/tests",
    }

    response = client.post("api/v0/assets/", json=body)
    data = response.json()

    assert response.status_code == 200
    # assert elements we can't know the value are not none
    assert response.json()["id"]
    assert response.json()["created_at"]
    assert response.json()["updated_at"]
    # assert result is user defined data + server defined data
    assert data == {
        **body,
        **{
            "id": response.json()["id"],
            "created_at": response.json()["created_at"],
            "updated_at": response.json()["updated_at"],
        },
    }


def test_create_asset_invalid(client: TestClient):
    # No required attribute type
    body = {"name": "test_img", "latest_version": 0.1, "file_path": "/tests"}

    response = client.post("api/v0/assets/", json=body)
    assert response.status_code == 422

    # extra parameter extra
    body = {
        "extra": "test_extra",
        "type": "image",
        "name": "test_img",
        "latest_version": 0.1,
    }

    response = client.post("api/v0/assets/", json=body)
    assert response.status_code == 422

    # type not in available types
    body = {"type": "other", "name": "test_img", "latest_version": 0.1}
    response = client.post("api/v0/assets/", json=body)
    assert response.status_code == 422


def test_read_assets(session: Session, client: TestClient):
    asset_1 = Asset(
        name="first_asset",
        latest_version=0.1,
        file_path="/test",
        type=AssetType.IMAGE,
    )
    asset_2 = Asset(
        name="snd_asset",
        latest_version=1.1,
        file_path="/test/data",
        type=AssetType.SOUND,
    )
    session.add(asset_1)
    session.add(asset_2)
    session.commit()

    response = client.get("api/v0/assets/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data == [
        {
            **asset_1.model_dump(exclude={"model_version"}),
            **{
                "id": response.json()[0]["id"],
                "created_at": response.json()[0]["created_at"],
                "updated_at": response.json()[0]["updated_at"],
            },
        },
        {
            **asset_2.model_dump(exclude={"model_version"}),
            **{
                "id": response.json()[1]["id"],
                "created_at": response.json()[1]["created_at"],
                "updated_at": response.json()[1]["updated_at"],
            },
        },
    ]


def test_read_assets_limit_offset(session: Session, client: TestClient):
    asset_1 = Asset(
        name="first_asset",
        latest_version=0.1,
        file_path="/test",
        type=AssetType.IMAGE,
    )
    asset_2 = Asset(
        name="snd_asset",
        latest_version=1.1,
        file_path="/test/data",
        type=AssetType.SOUND,
    )
    session.add(asset_1)
    session.add(asset_2)
    session.commit()

    # read the first asset
    response = client.get("api/v0/assets?limit=1&offset=0")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 1
    assert data == [
        {
            **asset_1.model_dump(exclude={"model_version"}),
            **{
                "id": response.json()[0]["id"],
                "created_at": response.json()[0]["created_at"],
                "updated_at": response.json()[0]["updated_at"],
            },
        },
    ]

    # read the second asser
    response = client.get("api/v0/assets?limit=1&offset=1")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 1
    assert data == [
        {
            **asset_2.model_dump(exclude={"model_version"}),
            **{
                "id": response.json()[0]["id"],
                "created_at": response.json()[0]["created_at"],
                "updated_at": response.json()[0]["updated_at"],
            },
        },
    ]


def test_read_asset(session: Session, client: TestClient):
    asset = Asset(
        name="first_asset",
        latest_version=0.1,
        file_path="/test",
        type=AssetType.IMAGE,
    )
    session.add(asset)
    session.commit()

    response = client.get("api/v0/assets/1")
    data = response.json()

    assert response.status_code == 200
    assert data == {
        **asset.model_dump(exclude={"model_version"}),
        **{
            "id": response.json()["id"],
            "created_at": response.json()["created_at"],
            "updated_at": response.json()["updated_at"],
        },
    }


def test_patch_asset(session: Session, client: TestClient):
    asset = Asset(
        name="first_asset",
        latest_version=0.1,
        file_path="/test",
        type=AssetType.IMAGE,
    )
    session.add(asset)
    session.commit()

    body = {
        "name": "updated_name",
    }
    response = client.patch("api/v0/assets/1", json=body)
    data = response.json()

    assert response.status_code == 200
    assert data == {
        **asset.model_dump(exclude={"model_version"}),
        # update with patch data
        **body,
        # update with server created data
        **{
            "id": response.json()["id"],
            "created_at": response.json()["created_at"],
            "updated_at": response.json()["updated_at"],
        },
    }


def test_patch_asset_invalid(session: Session, client: TestClient):
    asset = Asset(
        name="first_asset",
        latest_version=0.1,
        file_path="/test",
        type=AssetType.IMAGE,
    )
    session.add(asset)
    session.commit()

    # type is a create only attribute
    body = {
        "type": "sound",
    }
    response = client.patch("api/v0/assets/1", json=body)
    assert response.status_code == 422


def test_delete_asset(session: Session, client: TestClient):
    asset = Asset(
        name="first_asset",
        latest_version=0.1,
        file_path="/test",
        type=AssetType.IMAGE,
    )
    session.add(asset)
    session.commit()

    response = client.delete("api/v0/assets/1")

    asset_in_db = session.get(Asset, 1)

    assert response.status_code == 200

    assert asset_in_db is None
