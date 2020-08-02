import { useRouter } from 'next/router';
import Alert from 'react-bootstrap/Alert';
import { toast } from 'react-toastify';
import apiClient from 'services/api';
import LoadingIcon from 'components/widgets/LoadingIcon';

const AuthContext = React.createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = React.useState(null);
  const [error, setError] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const router = useRouter();

  const verifyTokenAndFetchUser = async () => {
    const verified = await apiClient.verifyToken();
    if (verified) {
      await fetchUser();
    }
    setLoading(false);
  };

  React.useEffect(() => {
    verifyTokenAndFetchUser();
  }, []);

  const login = async (username, password) => {
    let { data, error } = await apiClient.login(username, password);
    if (data) {
      setUser(data);
    } else {
      toast.error(error);
    }
    router.push('/');
  };

  const logout = () => {
    apiClient.logout();
    setUser(null);
    router.push('/login');
  };

  const fetchUser = async () => {
    const { data, error } = await apiClient.authenticatedGet('user/');
    if (data) {
      setUser(data);
    } else {
      setError(error);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!user,
        user,
        fetchUser,
        login,
        logout,
        loading,
        error,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => React.useContext(AuthContext);

export const PrivateRoute = Component => {
  return () => {
    const { isAuthenticated, loading, error } = useAuth();
    const router = useRouter();

    React.useEffect(() => {
      if (!isAuthenticated && !loading) {
        router.push('/login');
      }
    }, [isAuthenticated, loading]);

    if (error) {
      return <Alert variant={'danger'}>{error}</Alert>;
    } else if (loading) {
      return <LoadingIcon />;
    } else if (!isAuthenticated) {
      return <div>Not authenticated</div>;
    }

    return <Component />;
  };
};

export default useAuth;
