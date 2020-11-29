import Modal from 'react-bootstrap/Modal';
import SetEmailForm from 'components/auth/SetEmailForm';

export default ({ showModal, setShowModal, onSubmit }) => {
  return (
    <Modal show={showModal} onHide={() => setShowModal(false)}>
      <Modal.Body>
        <SetEmailForm onSubmit={onSubmit} setShowModal={setShowModal} />
      </Modal.Body>
    </Modal>
  );
};
