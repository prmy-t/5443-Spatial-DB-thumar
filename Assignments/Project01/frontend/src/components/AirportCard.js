import { Row, Col, Card } from "react-bootstrap";
export default function AirportCard(props) {
  const airport = props.airport;

  return (
    <Card>
      <Card.Header className="h5">
        {airport.id}: {airport.name}
      </Card.Header>
      <Card.Body>
        <Card.Text>
          <Row>
            <Col md={6}>
              <b>Country:</b> {airport.country}
            </Col>
            <Col>
              <b> City:</b> {airport.city}
            </Col>
          </Row>
        </Card.Text>
        <Card.Text>
          <Row>
            <Col className="h6">
              <b> 3-Code:</b> {airport["3-code"]}
            </Col>
            <Col className="h6">
              <b> 4-Code:</b> {airport["4-code"]}
            </Col>
          </Row>
        </Card.Text>
        <Row>
          <Col>
            <Card.Text>
              <b>Lat: </b>
              {airport.lat}
            </Card.Text>
          </Col>
          <Col>
            <Card.Text>
              <b>Lon:</b> {airport.lon}
            </Card.Text>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
}
