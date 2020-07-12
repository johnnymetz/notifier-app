import { useRouter } from 'next/router';
import Layout from 'components/Layout';
import UserDetail from 'components/UserDetail';
import { protectRoute } from 'helpers';

export default () => {
  const router = useRouter();

  React.useEffect(() => {
    protectRoute(router);
  }, []);

  return (
    <Layout>
      <UserDetail />
    </Layout>
  );
};
