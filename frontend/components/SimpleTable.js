import Table from 'react-bootstrap/Table';

export default ({ userData }) => {
  return (
    <>
      <div>Simple Table</div>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Name</th>
            <th>Birthday</th>
            <th>Age</th>
          </tr>
        </thead>
        <tbody>
          {userData.friends.results.map(friend => (
            <tr key={friend.id}>
              <td>
                {friend.first_name} {friend.last_name}
              </td>
              <td>{friend.birthday}</td>
              <td>{friend.age}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </>
  );
};
