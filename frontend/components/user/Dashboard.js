import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import useAuth from 'contexts/auth';
import AddFriend from 'components/friend/AddFriend';
import UpcomingList from 'components/friend/UpcomingFriendsList';
import FriendsTable from 'components/friend/FriendsTable';

export default () => {
  const { user } = useAuth();

  return (
    <>
      <Row className="mb-4">
        <Col md={6}>
          <Card body className="shadow">
            <UpcomingList friends={user.upcoming_friends} />
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
        <FriendsTable friends={user.all_friends} />
      </Card>
    </>
  );
};
