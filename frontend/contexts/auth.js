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

  const signup = async (email, password, re_password, setFieldError) => {
    let { data, error } = await apiClient.createUser(
      email,
      password,
      re_password
    );
    if (data) {
      router.push('/login');
      toast.success(
        'Your account was successfully created! Check your email to activate it.'
      );
    } else {
      console.warn(error);
      // consolidate into a single helper that parses response and sets error appropriately
      if (error.email) {
        setFieldError('email', error.email[0]);
      }
      if (error.password) {
        setFieldError('password', error.password[0]);
      }
      if (error.re_password) {
        setFieldError('re_password', error.re_password[0]);
      }
      if (error.non_field_errors) {
        toast.error(error.non_field_errors[0]);
      }
      if (typeof error === 'string') {
        toast.error(error);
      }
    }
  };

  const activate = async (uid, token) => {
    const { error } = await apiClient.activateUser(uid, token);
    if (error) {
      console.warn(error);
      toast.error(
        (error.uid && error.uid[0]) ||
          (error.token && error.token[0]) ||
          'Unable to activate user account'
      );
    } else {
      router.push('/');
      toast.success(
        'User account successfully activated. Please login to get started.'
      );
    }
  };

  const fetchUser = async () => {
    const { data, error } = await apiClient.authenticatedGet('auth/users/me/');
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
        loading,
        error,
        fetchUser,
        login,
        logout,
        signup,
        activate,
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
