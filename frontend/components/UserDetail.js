import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import useAuth from 'contexts/auth';
import AddFriend from 'components/AddFriend';
import UpcomingList from 'components/UpcomingList';
import FriendsTable from 'components/FriendsTable';

export default () => {
  const { user } = useAuth();

  return (
    <div>
      <h2>Welcome, {user.username}</h2>
      <hr />
      <Row>
        <Col>
          <AddFriend />
        </Col>
        <Col>
          <UpcomingList friends={user.upcoming_friends} />
        </Col>
      </Row>
      <hr />
      <FriendsTable friends={user.all_friends} />
    </div>
  );
};
