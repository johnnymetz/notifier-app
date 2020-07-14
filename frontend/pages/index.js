import Layout from 'components/Layout';
import UserDetail from 'components/UserDetail';
import { PrivateRoute } from 'contexts/auth';

const Home = () => {
  return (
    <Layout>
      <UserDetail />
    </Layout>
  );
};

export default PrivateRoute(Home);
