import Dashboard from 'components/Dashboard';
import { PrivateRoute } from 'contexts/auth';

const Home = () => {
  return <Dashboard />;
};

export default PrivateRoute(Home);
