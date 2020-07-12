import React from 'react';
import Alert from 'react-bootstrap/Alert';
import { sendAuthenticatedGetRequest } from 'api';
import UpcomingList from 'components/UpcomingList';
import FriendsTable from 'components/FriendsTable';

export default () => {
  const [user, setUser] = React.useState(null);
  const [error, setError] = React.useState(null);

  const getUserData = async () => {
    const { error, data } = await sendAuthenticatedGetRequest('user/');
    if (error) {
      setError(error);
    } else {
      setUser(data);
    }
  };

  React.useEffect(() => {
    getUserData();
  }, []);

  if (error) {
    return <Alert variant={'danger'}>{error}</Alert>;
  } else if (!user) {
    return <div>Loading...</div>;
  }

  console.log(user);
  return (
    <div>
      <h2>Welcome, {user.username}</h2>
      <hr />
      <UpcomingList friendData={user.upcoming_friends} />
      <hr />
      <FriendsTable friendData={user.all_friends} />
    </div>
  );
};
