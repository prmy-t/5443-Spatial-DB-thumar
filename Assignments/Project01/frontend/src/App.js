import { useState, useEffect } from "react";
import "./App.css";
import {
  Button,
  Row,
  Col,
  Container,
  Form,
  InputGroup,
  Spinner,
} from "react-bootstrap";

import ErrorModal from "./components/ErrorModal";
import AirportCard from "./components/AirportCard";

function App() {
  useEffect(() => {
    document.title = "Airports";
  });
  //New One
  const [btnColor, setBtnColor] = useState("danger");
  const [isReady, setIsReady] = useState();
  const [query, setQuery] = useState();
  const [data, setData] = useState();
  const [error, setError] = useState();
  const [show, setShow] = useState();
  const [isLoading, setIsLoading] = useState(false);

  const makeDatabaseReady = async () => {
    const res = await fetch("http://localhost:8000/make-database-ready", {
      mode: "cors",
    });
    const data = await res.json();
    setIsReady(data);
    setBtnColor("success");
  };
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
    console.log(data);
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
        <hr className="mb-2" />
        <Row className="justify-content-end mb-3">
          <Col className="text-end mb-3" sm={6} md={4}>
            <Button onClick={makeDatabaseReady} variant={btnColor}>
              Make database ready
            </Button>
          </Col>
          {isReady &&
            isReady.map((line) => (
              <Col
                className="text-success text-end"
                md={12}
                lg={12}
                sm={12}
                key={line}
              >
                {line}
              </Col>
            ))}
        </Row>
        <hr />

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
        <Row className="mt-2 justify-content-center">
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

export default App;
