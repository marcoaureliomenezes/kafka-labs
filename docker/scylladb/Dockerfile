FROM scylladb/scylla:5.4



RUN mkdir /docker-entrypoint-initdb.d

COPY ./create_tables.cql /docker-entrypoint-initdb.d/create_keyspace.cql



COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
