# using the 15.2 version of the official PostgreSQL Docker image
FROM postgres:15.2
# sets the default user, password, and database name for the container
ENV POSTGRES_USER pg_user
ENV POSTGRES_PASSWORD pg_password
ENV POSTGRES_DB section2
# copy sql script to container's entrypoint directory to get executed during container startup
COPY ./create_table.sql /docker-entrypoint-initdb.d/