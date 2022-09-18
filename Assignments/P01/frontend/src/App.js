import { useState, useEffect } from "react";
import {
  Button,
  Row,
  Col,
  Container,
  Form,
  InputGroup,
  Spinner,
} from "react-bootstrap";
//File imports
import ErrorModal from "./components/ErrorModal";
import AirportCard from "./components/AirportCard";

export default function App() {
  useEffect(() => {
    document.title = "Airports";
  });
  //New One
  const [query, setQuery] = useState();
  const [data, setData] = useState();
  const [error, setError] = useState();
  const [show, setShow] = useState();
  const [isLoading, setIsLoading] = useState(false);

  const handleShow = () => {
    setShow(false);
  };
  const updateQuery = (event) => {
    setQuery(event.target.value);
  };
  const fireQuery = async () => {
    setIsLoading(true);
    const res = await fetch(`http://localhost:8000/?${query}`);
    const data = await res.json();
    if (data.length < 1) {
      setError("No Data Found !");
      setShow(true);
    } else setData(data);
    setIsLoading(false);
  };

  return (
    <>
      <Container className="mb-5 mt-3">
        <ErrorModal error={error} show={show} handleShow={handleShow} />
        <Row className="justify-content-center h2">
          <Col className="text-center" md={6}>
            Airports around the world
          </Col>
        </Row>
        <hr className="mb-4" />
        <Row>
          <Col>
            <Form.Label htmlFor="basic-url" className="text-muted">
              You can search the Airport by name, city, country, 3-code, 4-code,
              lat & lon.
            </Form.Label>
            <br />
            <Form.Label htmlFor="basic-url" className="text-muted">
              For example city = Calgary
            </Form.Label>
          </Col>
        </Row>
        <Row className="mt-4 justify-content-center">
          <Col md={10}>
            <InputGroup>
              <Form.Control
                onChange={updateQuery}
                placeholder="Start Typing..."
                id="basic-url"
              />
              <Button variant="primary" onClick={fireQuery}>
                Get
              </Button>
            </InputGroup>
          </Col>
        </Row>
      </Container>
      <Container className="mb-5" fluid="md">
        <Row className="justify-content-center my-4">
          {isLoading && <Spinner animation="border" variant="primary" />}
        </Row>
        <Row className="justify-content-center">
          {data &&
            data.map((airport) => {
              return (
                <Col key={airport.id} className="mb-3" sm={10} md={6} lg={4}>
                  <AirportCard airport={airport} />
                </Col>
              );
            })}
        </Row>
      </Container>
    </>
  );
}
