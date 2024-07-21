from fake_data_generator import fakeClientGenerator
from functools import reduce
import psycopg2
import random


class PostgresCDCSeeder:


  def __init__(self, schema, table_name, pg_conn):
    self.schema = schema
    self.table_name = table_name
    pg_conn.autocommit = True
    self.pg_cursor = pg_conn.cursor()
    self.primary_key = schema["primaryKey"]
    self.pk_values = self.get_pk_values()

  def get_pk_values(self):
    self.pg_cursor.execute(f"SELECT {self.primary_key} FROM {self.table_name};")
    return [i[0] for i in self.pg_cursor.fetchall()]

  def generate_insert(self, data):
    values = [f"'{value}'" if type(value) == str else value for value in data.values()]
    query = f"""INSERT INTO {self.table_name} ({', '.join(data.keys())})
    VALUES ({reduce(lambda a, b: f'{a}, {b}' , values)});
    """
    self.pg_cursor.execute(query)
    self.pk_values = self.get_pk_values()
  
  def generate_update(self, data):
    field_to_update = random.choice(list(self.schema["columns"].keys()))
    value_to_update = data[field_to_update]
    value_to_update = f"'{value_to_update}'" if type(value_to_update) == str else value_to_update
    row_to_update = f"{field_to_update} = {value_to_update}"
    pk_to_update = random.choice(self.pk_values)
    query = f"""UPDATE {self.table_name}
    SET {row_to_update}
    WHERE {self.primary_key} = {pk_to_update};
    """
    self.pg_cursor.execute(query)
  
  def generate_delete(self):
    row_to_delete = random.choice(self.pk_values)
    query = f"""
    DELETE FROM {self.table_name}
    WHERE {self.primary_key} = {row_to_delete};
    """
    self.pg_cursor.execute(query)

if __name__ == "__main__":

  fake_client_generator = fakeClientGenerator()

  schema = fake_client_generator.get_client_schema()
  data = fake_client_generator.gen_client_row()
  table_name = "accounts.client"

  pg_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    host="postgres",
    password="postgres"
  )
  

  seeder = PostgresCDCSeeder(schema, table_name, pg_conn)

  for i in range(100000):
    if random.random() < 0.5:
      seeder.generate_insert(fake_client_generator.gen_client_row())
    if random.random() < 0.4:
      seeder.generate_update(fake_client_generator.gen_client_row())
    if random.random() < 0.4:
      seeder.generate_delete()

  print("FIM")
  # INSERT A ROW

  # pg_cursor.execute(seeder.generate_insert(data))
  # pg_conn.commit()
  