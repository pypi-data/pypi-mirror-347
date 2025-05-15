# Cypher Query Loader

A small package that handles loading strings from `*.cypher` files into python strings.  I use this code in packages that query a database and need saved queries.  It lets me keep the code in `.cypher` format and use syntax highlighing in my IDE.

<strong>Important safety note:</strong>This code does not check cypher files for safety or security. End users should only point their QueryLoader objects at file systems they trust and control.

## Use

To use the CypherQueries object create an instance pointed at a directory of *.cypher files.  The CypherQueries object will add the *.cypher file names as attributes, so `<MY_FILE_PATH>/cypher/fetch_k_nodes.cypher` will become `queries.fetch_k_nodes` in the `CypherQueries` instance `queries`.

To return the query text you simply call the `queries.fetch_k_nodes` attribute.

The CypherLoader object automatically detects parameters in the query. To see the parameters of a query use the `params` attribute, eg `queries.fetch_k_nodes.params`.


```python
import cypher_query_loader

# The example is the packages tests
# Replace the example with a file to your packages cypher queries.
queries = cypher_query_loader.CypherQueries('./tests/cypher')

# return the query text
queries.fetch_k_nodes
# MATCH (n) RETURN n LIMIT $limit;

# return parameters of the query
queries.fetch_k_nodes.params
# {'limit': None}

# set parameters of the query
queries.fetch_k_nodes.params['limit'] = 5

queries.fetch_k_nodes.params
# {'limit': 5}
```

## Using the CypherQueries object with the `neo4j` package.
The queries can be fed directly to the `GraphDatabase.driver.execute_query()` function.

```python
from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")

driver = GraphDatabase.driver(uri, auth=AUTH)

result = driver.execute_query(
    queries.fetch_k_nodes,
    **query.fetch_k_nodes.params
    )

driver.close
```