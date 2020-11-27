import ListGroup from 'react-bootstrap/ListGroup';

const FriendsListItem = ({ friend, highlight = false }) => {
  const currentYear = new Date().getFullYear();
  const date = new Date(
    `${friend.date_of_birth.month}/${friend.date_of_birth.day}/${currentYear}`
  );
  const dateString = date.toLocaleDateString(undefined, {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  });
  return (
    <ListGroup.Item variant={highlight && 'info'}>
      {friend.age ? (
        <span>
          <b>{friend.name}</b> is turning {friend.age} on {dateString}
        </span>
      ) : (
        <span>
          <b>{friend.name}</b> has a birthday on {dateString}
        </span>
      )}
    </ListGroup.Item>
  );
};

const FriendsListGroup = ({
  friends_with_birthday_today,
  friends_with_birthday_upcoming,
}) => (
  <ListGroup>
    {friends_with_birthday_today.map(friend => (
      <FriendsListItem key={friend.id} friend={friend} highlight={true} />
    ))}
    {friends_with_birthday_upcoming.map(friend => (
      <FriendsListItem key={friend.id} friend={friend} />
    ))}
  </ListGroup>
);

export default ({
  friends_with_birthday_today,
  friends_with_birthday_upcoming,
}) => {
  return (
    <>
      <h5 className="text-center">Upcoming</h5>
      {friends_with_birthday_today.length > 0 ||
      friends_with_birthday_upcoming.length > 0 ? (
        <FriendsListGroup
          friends_with_birthday_today={friends_with_birthday_today}
          friends_with_birthday_upcoming={friends_with_birthday_upcoming}
        />
      ) : (
        <div className="text-center mt-3">No upcoming birthdays</div>
      )}
    </>
  );
};
