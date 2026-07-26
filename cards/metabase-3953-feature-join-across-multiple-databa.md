# Feature: Join across multiple databases

source: https://github.com/metabase/metabase/issues/3953
repo: metabase/metabase
+1s: 2107 | comments: 50 | opened: 2016-12-14

## Gap
Analysts need to join tables that live in different databases without standing up a full warehouse.

## Why host won't
Metabase published an official Learn post explaining they will not pull data into Metabase to join across DBs - they are not a query engine/storage layer, and they point users to warehouses, FDWs, or federated engines instead.

## Product angle
A thin federation / sync sidecar aimed at Metabase users: connect 2-3 sources, materialize joinable views into one warehouse Metabase already speaks (Postgres/DuckDB/BigQuery), with a UI that matches Metabase mental models. Sell the 'I just want the join' path, not another BI tool.

## Competition / workarounds
Full warehouses (Snowflake etc.), Trino/Starburst/Athena, Postgres FDWs. Gap is the Metabase-native, low-ops middle for teams that refuse a warehouse project.

## Kill if
Metabase ships native cross-DB joins, or <3 design partners pay for the sidecar after concierge.
