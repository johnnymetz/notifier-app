import ListGroup from 'react-bootstrap/ListGroup';

const EventsListItem = ({ event, today = false }) => {
  const currentYear = new Date().getFullYear();
  const date = new Date(
    `${event.annual_date.month}/${event.annual_date.day}/${currentYear}`
  );
  const dateString = date.toLocaleDateString(undefined, {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  });

  return (
    <ListGroup.Item variant={today && 'warning'}>
      {event.annual_date.year ? (
        <span>
          <b>{event.name}</b> is turning{' '}
          {today ? `${event.age} today` : `${event.age + 1} on ${dateString}`}
        </span>
      ) : (
        <span>
          <b>{event.name}</b> has a birthday{' '}
          {today ? 'today' : `on ${dateString}`}
        </span>
      )}
    </ListGroup.Item>
  );
};

const EventsListGroup = ({ events_today, events_upcoming }) => (
  <ListGroup>
    {events_today.map(event => (
      <EventsListItem key={event.id} event={event} today={true} />
    ))}
    {events_upcoming.map(event => (
      <EventsListItem key={event.id} event={event} />
    ))}
  </ListGroup>
);

export default ({ events_today, events_upcoming }) => {
  return (
    <>
      <h5 className="text-center">Upcoming Events</h5>
      {events_today.length > 0 || events_upcoming.length > 0 ? (
        <EventsListGroup
          events_today={events_today}
          events_upcoming={events_upcoming}
        />
      ) : (
        <div className="text-center mt-3">No upcoming events</div>
      )}
    </>
  );
};
