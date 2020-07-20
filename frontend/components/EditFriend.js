import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import FriendForm from 'components/FriendForm';

export default ({ show, setShow, friendValues }) => {
  return (
    <Modal show={show} onHide={() => setShow(false)}>
      <Modal.Header closeButton>
        <Modal.Title>Modal heading</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <h2>Edit Friend</h2>
        <FriendForm requestMethod={'PATCH'} friendValues={friendValues} />
      </Modal.Body>
      {/* <Modal.Footer>
        <Button variant="secondary" onClick={() => setShow(false)}>
          Close
        </Button>
        <Button variant="primary" onClick={() => console.log('Submitting')}>
          Save Changes
        </Button>
      </Modal.Footer> */}
    </Modal>
  );
};
