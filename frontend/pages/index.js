import Layout from 'components/Layout';
import { fetchData } from 'api';
import SimpleTable from 'components/SimpleTable';
import ReactTableDemo from 'components/ReactTableDemo';
import FriendsTable from 'components/FriendsTable';

export default ({ userData }) => {
  console.log(userData);
  return (
    <Layout>
      <FriendsTable data={userData.friends} />
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
