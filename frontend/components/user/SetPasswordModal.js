import Modal from 'react-bootstrap/Modal';
import SetPasswordForm from 'components/user/SetPasswordForm';

export default ({ showModal, setShowModal, onSubmit }) => {
  return (
    <Modal show={showModal} onHide={() => setShowModal(false)}>
      <Modal.Body>
        <SetPasswordForm onSubmit={onSubmit} setShowModal={setShowModal} />
      </Modal.Body>
    </Modal>
  );
};
