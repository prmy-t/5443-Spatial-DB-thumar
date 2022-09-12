const { Client } = require("pg");
const express = require("express");
const cors = require("cors");
const app = express();
app.use(cors());

//Connection
const client = new Client({
  host: "localhost",
  port: "5432",
  database: "project1",
  user: "postgres",
  password: "221702",
});
client.connect();

//Queries
const sql = {
  drop_table: `DROP TABLE airports;`,
  create_table: `
        CREATE TABLE public.airports
        (
            id smallint,
            name text,
            city text,
            country text,
            "3-code" text,
            "4-code" text, 
            geom geometry,
            lat float(8),
            lon float(8),
            elevation smallint,
            gmt text,
            tz_short text, 
            timezone text, 
            type text
        );
    `,
  copy_csv: `
    copy airports(id, name, city, country, "3-code", "4-code", lat, lon, elevation, gmt, tz_short, timezone, type) 
    from '/Users/prmy/Documents/5443-Spatial-DB-thumar/Assignments/Project01/airports.csv'
    with delimiter ',' csv header;
    `,
  update_geom: `
    UPDATE airports SET geom = ST_SetSRID(ST_MakePoint(lon,lat), 4326);
    `,
};

//API
//Make Database Ready
app.get("/make-database-ready", (req, res) => {
  let ready = [];
  client.query(sql.drop_table, (err, resp) => {
    if (!err) ready.push("Table dropped successfully.");
    else console.log(err);
    client.end;
  });
  client.query(sql.create_table, (err, resp) => {
    if (!err) {
      ready.push("Table Created successfully.");
    } else console.log(err);
    client.end;
  });
  client.query(sql.copy_csv, (err, resp) => {
    if (!err) ready.push("Table copied from CVS file.");
    else console.log(err);
    client.end;
  });
  client.query(sql.update_geom, (err, resp) => {
    if (!err) {
      ready.push("Updated GEOMETRY datatype successfully.");
      res.send(ready);
    } else console.log(err);
  });
});

//Queries
app.get("/", (req, res) => {
  const keys = Object.keys(req.query);
  const values = Object.values(req.query);
  let query = ``;
  if (keys.length > 1) {
    let [v1, v2] = [...values];
    v1 = v1.trim();
    v2 = v2.trim();
    query = `SELECT id,A.geom,ST_Distance (A.geom, ST_SetSRID(ST_Point (${v2}, ${v1}) ,4326)) as distance, name, city, country,"3-code","4-code",lat, lon FROM airports as A WHERE ST_Distance (A.geom, ST_SetSRID(ST_Point (${v2}, ${v1}), 4326)) < 10000 order by distance LIMIT 1`;
  } else {
    let k1 = keys[0].trim();
    let v1 = values[0].trim();
    if (k1.includes("limit") || k1.includes("offset"))
      query = `SELECT * FROM airports ${k1}`;
    else query = `SELECT * FROM airports where "${k1}"~*'${v1}'`;
  }
  //Firing Query
  client.query(query, (err, result) => {
    if (!err) {
      res.send(result.rows);
    } else {
      console.log(err);
      res.send([]);
    }
    client.end;
  });
});

app.listen(8000, () => {
  console.log("listening...");
});
