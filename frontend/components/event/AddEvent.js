import EventForm from 'components/event/EventForm';

export default () => {
  return (
    <>
      <h5 className="text-center">Add an Event</h5>
      <EventForm action={'create'} />
    </>
  );
};
