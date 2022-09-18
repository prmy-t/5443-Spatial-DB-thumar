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
//Making Database Ready
client.query(sql.drop_table, (err, res) => {
  if (err) console.log(err);
  client.end;
});
client.query(sql.create_table, (err, res) => {
  if (err) console.log(err);
  client.end;
});
client.query(sql.copy_csv, (err, res) => {
  if (err) console.log(err);
  client.end;
});
client.query(sql.update_geom, (err, res) => {
  if (err) console.log(err);
  client.end;
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
    query = `SELECT * from (
SELECT *, ST_DistanceSphere(ST_MakePoint(${v2}, ${v1}),ST_MakePoint(lon, lat))*0.000621371 as distance from airports A)
as innerTable ORDER BY distance asc LIMIT 1`;
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
