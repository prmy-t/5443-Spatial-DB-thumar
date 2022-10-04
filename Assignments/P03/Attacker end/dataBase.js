const { Client } = require("pg");
//Connection
const client = new Client({
  host: "localhost",
  port: "5432",
  database: "project3",
  user: "postgres",
  password: "221702",
});
client.connect();

exports.register_missiles = (num_of_missiles, res) => {
  const sql = `SELECT ST_x(
                 
                  (
                  
                  ST_Dump(
                  ST_GeneratePoints(geom, ${num_of_missiles * 2}, 1996)
                  )
                )
                .geom
               
              )
              as x,
              ST_y(
               
                (ST_Dump(
                  
                ST_GeneratePoints(geom, ${num_of_missiles * 2}, 1996)
                
                
                )
              
              
              ).geom) as y
FROM (
SELECT ST_Buffer(
	ST_GeomFromText('SRID=4326;LINESTRING(-129.784 19.743,-61.951 19.743, -61.951 54.345,-129.784 54.345)'),
  8, 'endcap=round join=round')  As geom ) as s;
  `;

  // first query
  const data = client.query(sql, (err, res1) => {
    if (!err) {
      const data = res1.rows;
      // second query
      client.query(
        `create table if not exists missiles_position(name text, starts geometry, ends geometry, altitude smallint, time_stamp time);   
        `,
        (err, res2) => {
          if (!err) {
            for (let i = 0; i < data.length / 2; i++) {
              client.query(
                `insert into missiles_position
                values(
                  '${generate_name()}', 
                  ST_SetSRID(ST_MakePoint(${data[i].x}, ${data[i].y}),4326)
                  
                  ,
                  ST_SetSRID(ST_MakePoint(${data[data.length / 2 + i].x}, ${
                  data[data.length / 2 + i].y
                }),4326),
                  ${Math.floor(Math.random() * (12000 - 10000) + 10000)},
                  current_time
                  )`,

                (err, res3) => {
                  if (!err) {
                  } else console.log(err);
                }
              );
            }
            client.query(
              `select * from missiles_position INNER JOIN missiles_info on missiles_position.name = missiles_info.name order by time_stamp DESC limit ${num_of_missiles}`,
              (err, res1) => {
                if (!err) res.send(res1.rows);
                else console.log(err);
              }
            );
          } else console.log(err);
        }
      );

      return res.rows;
    } else console.log(err);
    client.end;
  });
  return data;
};

exports.calculate_hits = (a, res) => {
  `
  select ST_AsGeoJSON(
	ST_Intersection(
		b.area,
		'LINESTRING(
            m., -104.04052734375  38.839707613545144
          )'::geometry))
  
  
  `;
};

const generate_name = () => {
  const names = [
    "m01",
    "m02",
    "m03",
    "m04",
    "m05",
    "m06",
    "m07",
    "m08",
    "m09",
    "m10",
  ];
  const num = Math.floor(Math.random() * 9);
  return names[num];
};
