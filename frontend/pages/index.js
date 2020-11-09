import Dashboard from 'components/user/Dashboard';
import { PrivateRoute } from 'contexts/auth';

const Home = () => {
  return <Dashboard />;
};

export default PrivateRoute(Home);
