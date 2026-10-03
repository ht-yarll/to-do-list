FROM postgres:18-alpine

# Make the database container's runtime identity explicit.
USER postgres

EXPOSE 5432
