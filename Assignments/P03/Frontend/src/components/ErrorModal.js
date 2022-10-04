import { Modal, Button } from "react-bootstrap";

export default function ErrorModal(props) {
  return (
    <Modal show={props.show} onHide={props.handleShow}>
      <Modal.Header closeButton>
        <Modal.Title>Error</Modal.Title>
      </Modal.Header>
      <Modal.Body>{props.error}</Modal.Body>
      <Modal.Footer>
        <Button variant="danger" onClick={props.handleShow}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
}
