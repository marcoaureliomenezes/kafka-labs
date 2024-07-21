CREATE SCHEMA IF NOT EXISTS accounts;
CREATE TABLE IF NOT EXISTS accounts.client (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  age INT, 
  salary FLOAT,
  status VARCHAR(255),
  city VARCHAR(255),
  state VARCHAR(255));