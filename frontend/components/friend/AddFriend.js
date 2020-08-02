import FriendForm from 'components/friend/FriendForm';

export default () => {
  return (
    <div>
      <h4>Add Friend</h4>
      <FriendForm requestMethod={'POST'} />
    </div>
  );
};
