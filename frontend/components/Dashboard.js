import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

import useAuth from 'contexts/auth';
import AddEvent from 'components/event/AddEvent';
import UpcomingEventsList from 'components/event/UpcomingEventsList';
import EventsList from 'components/event/EventsList';

export default () => {
  const { user } = useAuth();

  return (
    <>
      <Row className="mb-4">
        <Col md={6}>
          <Card body className="shadow">
            <UpcomingEventsList
              events_today={user.events_today}
              events_upcoming={user.events_upcoming}
            />
          </Card>
          <div className="d-sm-block d-md-none mb-4"></div>
        </Col>
        <Col md={6}>
          <Card body className="shadow">
            <AddEvent />
          </Card>
        </Col>
      </Row>
      <Card body className="shadow">
        <EventsList events={user.all_events} />
      </Card>
    </>
  );
};
