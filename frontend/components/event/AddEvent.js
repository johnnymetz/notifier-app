import EventForm from 'components/event/EventForm';

const AddEvent = () => {
  return (
    <>
      <h5 className="text-center">Add an Event</h5>
      <EventForm action={'create'} />
    </>
  );
};

export default AddEvent;
