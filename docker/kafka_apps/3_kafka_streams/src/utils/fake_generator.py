from random import choice, randint
from faker import Faker
from typing import Dict, List
from functools import reduce

class FakeGenerator:

  def __init__(self):
    self.faker = Faker(locale='pt_BR')

  def gen_address(self, city, state):
    address = self.faker.address()
    return {
      "logradouro": address.split('\n')[0],
      "bairro": address.split('\n')[1],
      "cidade": city,
      "estado": state,
    }
  
  def gen_fair_choice(self, choices: Dict[str, float]):
    minima_chance = min(choices.values())
    normalized = {k: int(v/minima_chance) for k, v in choices.items()}
    fair_choice_list = reduce(lambda a, b: a + b, [[k for j in range(v)] for k, v in normalized.items()])
    return choice(fair_choice_list)
                  

  def fake_client(self):
    city = self.faker.city()
    state = self.faker.state_abbr()
    return {
      "id": randint(1, 100),
      "name": self.faker.name(),
      "cpf": self.faker.cpf(),
      "graduation": self.gen_fair_choice({'Ensino Fundamental': 0.45, 'Ensino Médio': 0.35, 'Ensino Superior': 0.15, 'Mestrado': 0.04, 'Doutorado': 0.01}),
      "status_civil": choice(['Solteiro', 'Casado', 'Divorciado', 'Viúvo']),
      "phones": [self.faker.phone_number() for i in range(randint(0,3))],
      "birthdate": self.faker.date_of_birth().strftime('%Y-%m-%d'),
      "address": [self.gen_address(city, state) for i in range(randint(1,2))]
    }
  

  def fake_block(self):
    return {
      "block_id": randint(1, 100),
      "txs": [self.faker.sha256() for i in range(randint(1,10))],
      "hash_id": self.faker.sha256()
    }

  def get_client_avro_schema(self):
    return {
      "type": "record",
      "name": "Client",
      "fields": [
        {
          "name": "id", 
          "type": "int"
        },{
          "name": "name",
          "type": "string"
        },{
          "name": "cpf",
          "type": "string"
        },{
          "name": "graduation",
          "type": "string"
        },{
          "name": "status_civil",
          "type": "string"
        },{
          "name": "phones",
          "type": {
            "type": "array", 
            "items": "string"
            }
        },{
          "name": "birthdate",
          "type": "string"
        },{
          "name": "address",
          "type": {
            "type": "array",
            "items": {
              "type": "record",
              "name": "Address",
              "fields": [
                {"name": "logradouro", "type": "string"},
                {"name": "bairro", "type": "string"},
                {"name": "cidade", "type": "string"},
                {"name": "estado", "type": "string"}
              ]
            }
          }
        }
      ]
    }
  

if __name__ == '__main__':
  fake_data_generator = FakeGenerator()
  print(fake_data_generator.fake_client())