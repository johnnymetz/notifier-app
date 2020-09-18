import { useState, useEffect, createContext, useContext } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'react-toastify';
import Alert from 'react-bootstrap/Alert';
import apiClient from 'services/api';
import LoadingIcon from 'components/widgets/LoadingIcon';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const verifyTokenAndFetchUser = async () => {
    const verified = await apiClient.verifyToken();
    if (verified) {
      await fetchUser();
    }
    setLoading(false);
  };

  useEffect(() => {
    verifyTokenAndFetchUser();
  }, []);

  const login = async (email, password) => {
    let { data, error } = await apiClient.login(email, password);
    if (data) {
      setUser(data);
      router.push('/');
    } else {
      toast.error(error);
    }
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

export const useAuth = () => useContext(AuthContext);

export const PrivateRoute = Component => {
  return () => {
    const { isAuthenticated, loading, error } = useAuth();
    const router = useRouter();

    useEffect(() => {
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
