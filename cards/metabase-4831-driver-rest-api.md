# Driver: REST API

source: https://github.com/metabase/metabase/issues/4831
repo: metabase/metabase
+1s: 888 | comments: 55 | opened: 2017-04-21

## Gap
Product/ops data lives behind REST APIs; people want it in Metabase without hand-rolled ETL.

## Why host won't
P2 New Feature for years; maintainer framed aggregation via REST as probably out of scope. Still open; users still asking in 2026.

## Product angle
Managed 'API → warehouse table' sync (schema inference, pagination, auth) optimized as a Metabase datasource - not a generic iPaaS. Start with OpenAPI-described APIs.

## Competition / workarounds
Airbyte/Fivetran/custom ETL, nano3ti/metabase-rest-api-driver (1 star). Sell Metabase-specific packaging + support.

## Kill if
Cannot get reliable schema inference on 5 real customer APIs, or Metabase ships an official HTTP driver.
