import Modal from 'react-bootstrap/Modal';
import FriendForm from 'components/friend/FriendForm';

export default ({ showModal, setShowModal, friendValues }) => {
  return (
    <Modal show={showModal} onHide={() => setShowModal(false)}>
      <Modal.Header closeButton>
        <Modal.Title>Edit Friend</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <FriendForm
          action={'update'}
          friendValues={friendValues}
          setShowModal={setShowModal}
        />
      </Modal.Body>
    </Modal>
  );
};
