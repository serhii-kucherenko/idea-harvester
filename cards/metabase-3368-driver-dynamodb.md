# Driver: DynamoDB

source: https://github.com/metabase/metabase/issues/3368
repo: metabase/metabase
+1s: 469 | comments: 29 | opened: 2016-09-17

## Gap
DynamoDB-backed products want Metabase analytics without Athena glue busywork.

## Why host won't
P2 New Feature since 2016; community points at Athena federation workarounds, not an official driver.

## Product angle
Turnkey DynamoDB → analytics path for Metabase (driver or managed sync to Postgres/Athena) aimed at startups already on Dynamo.

## Competition / workarounds
kawasima/metabase-dynamodb-driver (2 stars), Athena federation. Commercial support + DX is the wedge.

## Kill if
AWS/Metabase ship a blessed path that removes the pain for non-experts.
