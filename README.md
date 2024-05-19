# REPO-API

this API scrape the data from your github repositories and return to you

# Set up
```bash
touch config.json
echo {
    "postgres":{
        "server":"localhost",
        "database":"yourDatabaseName",
        "username":"yourUsername",
        "password":"yourPassword",
        "driver":"YourPostgresDriverName"
    }
    "gh-username":"YOUR_GITHUB_USERNAME"
} > config.json
```

- driver on ubuntu: psqlodbcw.so
- psqlodbca.so is getting error: mkleehammer/pyodbc#169

```sql
CREATE DATABASE yourDatabaseName;
```