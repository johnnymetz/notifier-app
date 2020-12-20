import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

import useAuth from 'contexts/auth';
import AddEvent from 'components/event/AddEvent';
import EventsListGroup from 'components/event/EventsListGroup';
import EventsTable from 'components/event/EventsTable';

export default () => {
  const {
    user: { events_today, events_upcoming, all_events },
  } = useAuth();

  return (
    <>
      <Row className="mb-4">
        <Col md={6}>
          <Card body className="mb-4">
            <h5 className="text-center">Today's Events</h5>
            {events_today.length > 0 ? (
              <EventsListGroup events={events_today} today={true} />
            ) : (
              <div className="text-center mt-3">No events today</div>
            )}
          </Card>
          <Card body className="mb-4">
            <h5 className="text-center">Upcoming Events</h5>
            {events_upcoming.length > 0 ? (
              <EventsListGroup events={events_upcoming} />
            ) : (
              <div className="text-center mt-3">No events upcoming</div>
            )}
          </Card>
          <div className="d-sm-block d-md-none mb-4"></div>
        </Col>
        <Col md={6}>
          <Card body>
            <AddEvent />
          </Card>
        </Col>
      </Row>
      <Card body>
        <h5 className="text-center">All Events</h5>
        <EventsTable events={all_events} />
      </Card>
    </>
  );
};
