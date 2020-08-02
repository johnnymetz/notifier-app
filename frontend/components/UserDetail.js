import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import useAuth from 'contexts/auth';
import AddFriend from 'components/friend/AddFriend';
import UpcomingList from 'components/friend/UpcomingFriendsList';
import FriendsTable from 'components/friend/FriendsTable';

export default () => {
  const { user } = useAuth();

  return (
    <div>
      <h2>Welcome, {user.username}</h2>
      <hr />
      <Row>
        <Col md={6}>
          <UpcomingList friends={user.upcoming_friends} />
          <hr className="d-sm-block d-md-none" />
        </Col>
        <Col md={6}>
          <AddFriend />
        </Col>
      </Row>
      <hr />
      <FriendsTable friends={user.all_friends} />
    </div>
  );
};
