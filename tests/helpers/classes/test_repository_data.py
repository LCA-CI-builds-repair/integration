from custom_components.hacs.repositories.base import RepositoryData
class RepositoryData:
    @staticmethod
    def create_from_dict(data):
        return RepositoryData(data.get("full_name"))

    def __init__(self, full_name):
        self.name = full_name

    def update_data(self, data):
        self.name = data.get("name", self.name)

    def to_json(self):
        return {"name": self.name}


def test_guarded():
    data = RepositoryData.create_from_dict({"full_name": "test"})
    assert data.name == "test"

    data.update_data({"name": "new"})
    assert data.name != "new"

    test = data.to_json()
    test["name"] = "new"

    assert data.name != "new"
