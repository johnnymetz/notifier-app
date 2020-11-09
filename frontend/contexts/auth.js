import { useState, useEffect, createContext, useContext } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'react-toastify';

import apiClient from 'services/api';
import { handleDrfError } from 'utils/helpers';
import LoadingIcon from 'components/widgets/LoadingIcon';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const verifyTokenAndFetchUser = async () => {
    setLoading(true);
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
      handleDrfError(error);
    }
  };

  const login = async (payload, setFieldError) => {
    let { data, error } = await apiClient.login(payload);
    if (data) {
      setUser(data);
      router.push('/');
    } else {
      handleDrfError(error, Object.keys(payload), setFieldError);
    }
  };

  const logout = () => {
    setLoading(true);
    apiClient.logout();
    setUser(null);
    router.push('/login');
    setLoading(false);
  };

  const createUser = async (payload, setFieldError) => {
    let { data, error } = await apiClient.createUser(payload);
    if (data) {
      router.push('/login');
      toast.success(
        'Your account was successfully created! Check your email to activate it.'
      );
    } else {
      handleDrfError(error, Object.keys(payload), setFieldError);
    }
  };

  const updateUser = async payload => {
    let { data, error } = await apiClient.updateUser(payload);
    if (data) {
      await fetchUser();
      toast.success('Your account was successfully updated');
    } else {
      handleDrfError(error);
    }
  };

  const activateUser = async payload => {
    const { error } = await apiClient.activateUser(payload);
    if (error) {
      handleDrfError(error);
    } else {
      router.push('/');
      toast.success(
        'Account successfully activated. Please login to get started.'
      );
    }
  };

  const setEmail = async (payload, setFieldError, setShowModal) => {
    const { error } = await apiClient.setEmail(payload);
    if (error) {
      handleDrfError(error, Object.keys(payload), setFieldError);
    } else {
      await fetchUser();
      setShowModal(false);
      toast.success('Email successfully changed');
    }
  };

  const setPassword = async (payload, setFieldError, setShowModal) => {
    const { error } = await apiClient.setPassword(payload);
    if (error) {
      handleDrfError(error, Object.keys(payload), setFieldError);
    } else {
      await fetchUser();
      setShowModal(false);
      toast.success('Password successfully changed');
    }
  };

  const sendResetPasswordEmail = async (payload, setFieldError) => {
    let { error } = await apiClient.sendResetPasswordEmail(payload);
    if (error) {
      handleDrfError(error, Object.keys(payload), setFieldError);
    } else {
      router.push('/login');
      toast.success('Check your email to reset your password');
    }
  };

  const resetPassword = async (payload, setFieldError) => {
    let { error } = await apiClient.resetPassword(payload);
    if (error) {
      handleDrfError(error, Object.keys(payload), setFieldError);
    } else {
      router.push('/login');
      toast.success('Password successfully updated. Please login to continue.');
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        fetchUser,
        login,
        logout,
        createUser,
        updateUser,
        activateUser,
        setEmail,
        setPassword,
        sendResetPasswordEmail,
        resetPassword,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

export const PrivateRoute = Component => {
  return () => {
    const { loading, user } = useAuth();
    const router = useRouter();

    useEffect(() => {
      if (!loading && !user) {
        router.push('/login');
      }
    }, [loading, user]);

    if (loading || !user) {
      return <LoadingIcon />;
    }

    return <Component />;
  };
};

export default useAuth;
