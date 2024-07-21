from faker import Faker


class fakeClientGenerator:

  def __init__(self):
    self.fake = Faker(locale="pt_BR")


  def gen_client_row(self):
    return {
      "name": self.fake.name(),
      "age": self.fake.random_int(min=18, max=99),
      "salary": self.fake.random_int(min=1000, max=10000),
      "status": self.fake.random_element(elements=("ACTIVE", "INACTIVE", "BLOCKED")),
      "city": self.fake.city(),
      "state": self.fake.state_abbr()
    }
  
  def get_client_schema(self):
    return {
      "primaryKey": "id",
      "columns": {
        "name": "string",
        "age": "int",
        "salary": "int",
        "status": "string",
        "city": "string",
        "state": "string"
      }
    }

