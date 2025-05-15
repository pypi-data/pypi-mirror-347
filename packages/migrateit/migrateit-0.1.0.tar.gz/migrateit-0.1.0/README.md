Handle database migrations with ease managing your database changes with simple SQL files.
Make the migration process easier, more manageable and repeteable.


# How does this work

### Installation
```sh
pip install migrateit
```

### Configuration
Configurations can be changed as environment variables.

```sh
# basic configuration
MIGRATIONS_TABLE=MIGRATEIT_CHANGELOG
MIGRATIONS_DIR=migrateit

# database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
```

### Usage

```sh
# initialize MigrateIt to create:
# - migrations table
# - migrations directory
# - migrations changelog
migrateit init

# create a new migration file
migrateit newmigration first_migration

# add your sql commands to the migration file
echo "CREATE TABLE test (id SERIAL PRIMARY KEY, name VARCHAR(50));" > migrateit/0001_first_migration.sql

# show pending migrations
migrateit showmigrations

# run the migrations
migrateit migrate
```
