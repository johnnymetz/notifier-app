import { useState, useEffect, createContext, useContext } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'react-toastify';
import Alert from 'react-bootstrap/Alert';
import apiClient from 'services/api';
import { handleDrfErrors } from 'utils/helpers';
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

  const fetchUser = async () => {
    const { data, error } = await apiClient.getCurrentUser();
    if (data) {
      setUser(data);
    } else {
      setError(error);
    }
  };

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
      handleDrfErrors(
        error,
        ['email', 'password', 're_password'],
        setFieldError
      );
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

  const setEmail = async (values, setFieldError, setShowModal) => {
    const { error } = await apiClient.setEmail(values);
    if (error) {
      handleDrfErrors(error, Object.keys(values), setFieldError);
    } else {
      await fetchUser();
      setShowModal(false);
      toast.success('User email successfully changed');
    }
  };

  const setPassword = async (values, setFieldError, setShowModal) => {
    const { error } = await apiClient.setPassword(values);
    if (error) {
      handleDrfErrors(error, Object.keys(values), setFieldError);
    } else {
      await fetchUser();
      setShowModal(false);
      toast.success('User email successfully changed');
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
        setEmail,
        setPassword,
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
