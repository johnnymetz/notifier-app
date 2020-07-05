import Table from 'react-bootstrap/Table';
import Layout from 'components/Layout';
import { fetchData } from 'api';

export default ({ userData }) => {
  console.log(userData);
  return (
    <Layout>
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
    </Layout>
  );
};

export async function getServerSideProps(context) {
  const { error, data } = await fetchData('users/1');
  if (error) {
    throw Error(error);
  }
  return {
    props: {
      userData: data,
    },
  };
}
