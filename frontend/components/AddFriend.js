import FriendForm from 'components/FriendForm';

export default () => {
  return (
    <div>
      <h4>Add Friend</h4>
      <FriendForm requestMethod={'POST'} />
    </div>
  );
};
