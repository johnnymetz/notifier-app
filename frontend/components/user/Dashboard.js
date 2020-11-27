import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

import useAuth from 'contexts/auth';
import AddFriend from 'components/friend/AddFriend';
import UpcomingFriendsList from 'components/friend/UpcomingFriendsList';
import FriendsList from 'components/friend/FriendsList';

export default () => {
  const { user } = useAuth();

  return (
    <>
      <Row className="mb-4">
        <Col md={6}>
          <Card body className="shadow">
            <UpcomingFriendsList
              friends_with_birthday_today={user.friends_with_birthday_today}
              friends_with_birthday_upcoming={
                user.friends_with_birthday_upcoming
              }
            />
          </Card>
          <div className="d-sm-block d-md-none mb-4"></div>
        </Col>
        <Col md={6}>
          <Card body className="shadow">
            <AddFriend />
          </Card>
        </Col>
      </Row>
      <Card body className="shadow">
        <FriendsList friends={user.all_friends} />
      </Card>
    </>
  );
};
