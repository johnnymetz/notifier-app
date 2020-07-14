import React from 'react';
import Alert from 'react-bootstrap/Alert';
import useAuth from 'contexts/auth';
import LoadingIcon from 'components/LoadingIcon';
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
      <UpcomingList friends={user.upcoming_friends} />
      <hr />
      <FriendsTable friends={user.all_friends} />
    </div>
  );
};
