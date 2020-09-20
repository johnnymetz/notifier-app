import { useEffect } from 'react';
import { useRouter } from 'next/router';
import useAuth from 'contexts/auth';
// import LoginBasic from 'components/auth/LoginBasic';
import LoginFormik from 'components/auth/LoginFormik';

export default () => {
  const { isAuthenticated, login } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated]);

  return (
    <>
      <h2>Login</h2>
      {/* <LoginBasic login={login} /> */}
      <LoginFormik login={login} />
    </>
  );
};
