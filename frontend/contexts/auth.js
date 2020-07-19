import { useRouter } from 'next/router';
import apiClient from 'services/api';

const AuthContext = React.createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = React.useState(null);
  const [error, setError] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const router = useRouter();

  React.useEffect(() => {
    const verifyTokenAndFetchUser = async () => {
      const verified = await apiClient.verifyToken();
      if (verified) {
        await fetchUser();
      }
      setLoading(false);
    };
    verifyTokenAndFetchUser();
  }, []);

  const login = async (username, password) => {
    setError(null);
    let { data, error } = await apiClient.login(username, password);
    if (data) {
      setUser(data);
    } else {
      setError(error);
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
