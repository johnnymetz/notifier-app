import { useRouter } from 'next/router';
import apiClient from 'services/api';

const AuthContext = React.createContext({});

export const AuthProvider = ({ children }) => {
  const [user, setUser] = React.useState(null);
  const [error, setError] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const router = useRouter();

  React.useEffect(() => {
    const verifyTokenAndLoadUser = async () => {
      const verified = await apiClient.verifyToken();
      if (verified) {
        const { data, error } = await apiClient.authenticatedGet('user/');
        if (data) {
          setUser(data);
        } else {
          setError(error);
        }
      }
      setLoading(false);
    };
    verifyTokenAndLoadUser();
  }, []);

  const login = async (username, password) => {
    setLoading(true);
    setError(null);
    let { data, error } = await apiClient.login(username, password);
    if (data) {
      setUser(data);
    } else {
      setError(error);
    }
    router.push('/');
    setLoading(false);
  };

  const logout = () => {
    setLoading(true);
    apiClient.logout();
    setUser(null);
    router.push('/login');
    setLoading(false);
  };

  return (
    <AuthContext.Provider
      value={{ isAuthenticated: !!user, user, login, logout, loading, error }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = React.useContext(AuthContext);
  return context;
};

export const PrivateRoute = Component => {
  return () => {
    const { isAuthenticated, loading } = useAuth();
    const router = useRouter();

    React.useEffect(() => {
      if (!isAuthenticated && !loading) {
        router.push('/login');
      }
    }, [isAuthenticated, loading]);

    return <Component />;
  };
};

export default useAuth;
