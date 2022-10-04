import { useState, useEffect } from "react";
import { Button, Col, Container, Row } from "react-bootstrap";
//File imports

export default function App() {
  const [missiles, setMissiles] = useState();
  useEffect(() => {
    document.title = "Boom";
  });

  const fireQuery = async () => {
    const res = await fetch("http://localhost:8000/get-missiles");
    const data = await res.json();
    console.log(data);
    setMissiles(data);
  };

  return (
    <>
      <Container className="m-5">
        <Row className="justify-content-start">
          <Col md={3}>
            <Button onClick={fireQuery}>Get missiles</Button>
          </Col>
          <Col md={3}>
            <Button onClick={fireQuery}>Calculate hits</Button>
          </Col>
        </Row>
      </Container>
      {missiles && (
        <Container>
          <Row>Get {missiles.length} Missiles !!</Row>
          <hr />
          {missiles.map((missile) => (
            <Row key={missile.starts.x} className="mt-4">
              <Col md={5}>Name: {missile.name}</Col>
              <Col md={5}>Speed: {missile.speed}</Col>
              <Col md={5}>Altitude: {missile.altitude}</Col>
              <Col md={5}>Fired at: {missile.time_stamp}</Col>
              <Col md={12}>
                Starting Point(x,y): {missile.starts.x}, {missile.starts.y}
              </Col>
              <Col md={12}>
                Ending Point: {missile.ends.x}, {missile.ends.y}
              </Col>
              <hr />
            </Row>
          ))}
        </Container>
      )}
    </>
  );
}
