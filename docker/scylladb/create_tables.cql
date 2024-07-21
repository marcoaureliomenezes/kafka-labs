CREATE KEYSPACE IF NOT EXISTS accounts WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE IF NOT EXISTS accounts.client (
  id INT PRIMARY KEY,
  name TEXT,
  age INT, 
  salary FLOAT,
  status TEXT,
  city TEXT,
  state TEXT);


  