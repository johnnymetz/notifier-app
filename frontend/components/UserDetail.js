import React from 'react';
import Alert from 'react-bootstrap/Alert';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import useAuth from 'contexts/auth';
import LoadingIcon from 'components/widgets/LoadingIcon';
import AddFriend from 'components/AddFriend';
import UpcomingList from 'components/UpcomingList';
import FriendsTable from 'components/FriendsTable';

export default () => {
  const { isAuthenticated, user, loading, error } = useAuth();

  if (error) {
    return <Alert variant={'danger'}>{error}</Alert>;
  } else if (loading || !isAuthenticated) {
    return <LoadingIcon />;
  }

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
