import ListGroup from 'react-bootstrap/ListGroup';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faBirthdayCake,
  faGlassCheers,
  faCalendarDay,
} from '@fortawesome/free-solid-svg-icons';

const getEventTypeIcon = eventType => {
  switch (eventType) {
    case 'Birthday':
      return faBirthdayCake;
    case 'Holiday':
      return faGlassCheers;
    default:
      return faCalendarDay;
  }
};

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
    <ListGroup.Item>
      <FontAwesomeIcon
        icon={getEventTypeIcon(event.type)}
        size={'sm'}
        style={{ marginRight: 10 }}
      />
      <b>{event.name}</b> {!today && `on ${dateString}`}
    </ListGroup.Item>
  );
};

const EventsListGroup = ({ events, today = false }) => (
  <ListGroup data-test={today ? 'today-events-list' : 'upcoming-events-list'}>
    {events.map(event => (
      <EventsListItem key={event.id} event={event} today={today} />
    ))}
  </ListGroup>
);

export default ({ events_today, events_upcoming }) => {
  return (
    <>
      <h5 className="text-center">Today's Events</h5>
      {events_today.length > 0 ? (
        <EventsListGroup events={events_today} today={true} />
      ) : (
        <div className="text-center mt-3">No events today</div>
      )}
      <h5 className="text-center mt-3">Upcoming Events</h5>
      {events_upcoming.length > 0 ? (
        <EventsListGroup events={events_upcoming} />
      ) : (
        <div className="text-center mt-3">No events upcoming</div>
      )}
    </>
  );
};
