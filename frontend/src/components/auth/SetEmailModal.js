import Modal from 'react-bootstrap/Modal';
import SetEmailForm from 'src/components/auth/SetEmailForm';

const SetEmailModal = ({ showModal, setShowModal, onSubmit }) => {
  return (
    <Modal show={showModal} onHide={() => setShowModal(false)}>
      <Modal.Body>
        <SetEmailForm onSubmit={onSubmit} setShowModal={setShowModal} />
      </Modal.Body>
    </Modal>
  );
};

export default SetEmailModal;
