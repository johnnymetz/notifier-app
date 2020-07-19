import ListGroup from 'react-bootstrap/ListGroup';

export default ({ friends }) => {
  return (
    <div>
      <h4>Upcoming</h4>
      {friends && friends.length > 0 ? (
        <ListGroup>
          {friends.map(friend => {
            const currentYear = new Date().getFullYear();
            const date = new Date(`${friend.birthday}/${currentYear}`);
            const dateString = date.toLocaleDateString(undefined, {
              weekday: 'long',
              month: 'long',
              day: 'numeric',
            });
            return (
              <ListGroup.Item key={friend.id}>
                {friend.first_name} {friend.last_name} is turning {friend.age}{' '}
                on {dateString}
              </ListGroup.Item>
            );
          })}
        </ListGroup>
      ) : (
        <div>No upcoming birthdays</div>
      )}
    </div>
  );
};
