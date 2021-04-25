import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import SubmitButton from 'components/widgets/SubmitButton';

const ConfirmModal = ({
  showModal,
  setShowModal,
  onConfirm,
  title,
  body,
  confirmButtonText,
  isSubmitting,
}) => {
  return (
    <Modal show={showModal} onHide={() => setShowModal(false)}>
      <Modal.Header closeButton>
        <Modal.Title>{title}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div>{body}</div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="outline-secondary" onClick={() => setShowModal(false)}>
          Cancel
        </Button>
        <SubmitButton
          onClick={onConfirm}
          isSubmitting={isSubmitting}
          variant={'danger'}
          data-test="confirm-modal-btn"
        >
          {confirmButtonText}
        </SubmitButton>
      </Modal.Footer>
    </Modal>
  );
};

export default ConfirmModal;
