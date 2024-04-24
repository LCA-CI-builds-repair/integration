fdef test_guarded():
    data = RepositoryData.create_from_dict({"full_name": "test"})
    assert data.name == "test"

    data.update_data({"name": "new"})
    assert data.name == "test"  # Verify that name remains unchanged after update_data

    test = data.to_json()
    test["name"] = "new"

    assert data.name == "test"  # Verify that name in data is not affected by changes in testmponents.hacs.repositories.base import RepositoryData


def test_guarded():
    data = RepositoryData.create_from_dict({"full_name": "test"})
    assert data.name == "test"

    data.update_data({"name": "new"})
    assert data.name != "new"

    test = data.to_json()
    test["name"] = "new"

    assert data.name != "new"
