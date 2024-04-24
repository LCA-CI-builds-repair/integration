from cusassert data.name != "new"

test = data.to_json()
test["name"] = "new"

data.update_data(test)

assert data.name == "new"mponents.hacs.repositories.base import RepositoryData


def test_guarded():
    data = RepositoryData.create_from_dict({"full_name": "test"})
    assert data.name == "test"

    data.update_data({"name": "new"})
    assert data.name != "new"

    test = data.to_json()
    test["name"] = "new"

    assert data.name != "new"
