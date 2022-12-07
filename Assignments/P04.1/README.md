# Description

## SQL folder

- Contains all the create script of tables.
- Data of all the tables are provided in [P04.2](https://github.com/prmy-t/5443-Spatial-DB-thumar/tree/main/Assignments/P04.2).

## api.py

- Used to get data from the server and create the postgres table.

- This is an older version of the code, which will get updated in upcoming projects...

## function.py

- Used as a supporting file of an api.py; to organize the code.

## final_product

- It contains the fine output of ship table after generating the location.
- for instance...

```
{
  "fleet_id": 0,
  "ship_status": [
    [
      [
        {
          "ship_id": 0,
          "bearing": 180,
          "location": { "lon": -4.659340223845248, "lat": 44.5433983730958 }
        }
      ],
      [
        {
          "ship_id": 1,
          "bearing": 180,
          "location": { "lon": -4.656546735993814, "lat": 44.543398338934054 }
        }
      ],
      ...
```
