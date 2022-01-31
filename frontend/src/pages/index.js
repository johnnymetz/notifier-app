import Dashboard from 'src/components/Dashboard';
import { PrivateRoute } from 'src/contexts/auth';

const Home = () => {
  return <Dashboard />;
};

export default PrivateRoute(Home);
