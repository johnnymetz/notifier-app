import Modal from 'react-bootstrap/Modal';
import EventForm from 'src/components/event/EventForm';

const EditEventModal = ({ showModal, setShowModal, eventValues }) => {
  return (
    <Modal show={showModal} onHide={() => setShowModal(false)}>
      <Modal.Header closeButton>
        <Modal.Title>Edit Event</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <EventForm
          action={'update'}
          eventValues={eventValues}
          setShowModal={setShowModal}
        />
      </Modal.Body>
    </Modal>
  );
};

export default EditEventModal;
