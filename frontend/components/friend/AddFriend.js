import FriendForm from 'components/friend/FriendForm';

export default () => {
  return (
    <>
      <h5 className="text-center">Add Friend</h5>
      <FriendForm action={'create'} />
    </>
  );
};
