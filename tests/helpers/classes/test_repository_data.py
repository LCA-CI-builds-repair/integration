from cus    # Check that the initial data name is not "new"
    assert data.name != "new"

    # Convert data to JSON, update the name, and check that the original data name is still not "new"
    test = data.to_json()
    test["name"] = "new"

    assert data.name != "new"mponents.hacs.repositories.base import RepositoryData


def test_guarded():
    data = RepositoryData.create_from_dict({"full_name": "test"})
    assert data.name == "test"

    data.update_data({"name": "new"})
    assert data.name != "new"

    test = data.to_json()
    test["name"] = "new"

    assert data.name != "new"
