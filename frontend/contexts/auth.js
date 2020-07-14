import { useRouter } from 'next/router';

import { axiosInstance, sendAuthenticatedGetRequest } from 'services/api';
import LoadingIcon from 'components/LoadingIcon';

const AuthContext = React.createContext({});

export const AuthProvider = ({ children }) => {
  const [user, setUser] = React.useState(null);
  const [error, setError] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const router = useRouter();

  React.useEffect(() => {
    console.log(user);
    const verifyTokenAndLoadUser = async () => {
      const verified = await _verifyToken();
      if (verified) {
        const { error, data } = await sendAuthenticatedGetRequest('user/');
        if (error) {
          setError(error);
        } else {
          setUser(data);
        }
      }
      setLoading(false);
    };
    verifyTokenAndLoadUser();
  }, []);

  const login = async (username, password) => {
    setLoading(true);
    setError(null);
    try {
      const res = await axiosInstance.post('token/', {
        username,
        password,
      });
      localStorage.setItem('accessToken', res.data.access);
      localStorage.setItem('refreshToken', res.data.refresh);
      // fetch user data
      const { data, error } = await sendAuthenticatedGetRequest('user/');
      if (data) {
        setUser(data);
      } else {
        setError(error);
      }
    } catch (err) {
      setError(err.response?.data.detail || err.toString());
    }
    setLoading(false);
    router.push('/');
  };

  const logout = () => {
    setLoading(true);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setUser(null);
    // window.location.pathname = '/login';
    setLoading(false);
    router.push('/login');
  };

  const _refreshToken = async () => {
    let refreshed = false,
      error;
    const refreshToken = localStorage.getItem('refreshToken');
    try {
      const res = await axiosInstance.post('token/refresh/', {
        refresh: refreshToken,
      });
      const data = res.data;
      localStorage.setItem('accessToken', data.access);
      refreshed = true;
      console.log('Token refreshed');
    } catch (err) {
      error = err.response?.data.detail || err.toString();
    }
    if (error) {
      console.log('Unable to refresh token');
    }
    return { refreshed, error };
  };

  const _verifyToken = async () => {
    let verified = false,
      error;
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      try {
        console.log('Verifying token...');
        await axiosInstance.post('token/verify/', {
          token: accessToken,
        });
        verified = true;
        console.log('Token verified');
      } catch (err) {
        if (err.response.status === 401) {
          const res2 = await _refreshToken();
          if (res2.refreshed) {
            verified = true;
          } else {
            error = res2.error;
          }
        } else {
          error = err.response?.data.detail || err.toString();
        }
      }
    } else {
      console.log('No token to verify');
    }
    if (error) {
      console.log(`Unable to verify token: ${error}`);
    }
    return verified;
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
