import UserDetail from 'components/UserDetail';
import { PrivateRoute } from 'contexts/auth';

const Home = () => {
  return <UserDetail />;
};

export default PrivateRoute(Home);
