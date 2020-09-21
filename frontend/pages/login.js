import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';

import useAuth from 'contexts/auth';
import LoginForm from 'components/auth/LoginForm';

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
      <LoginForm login={login} />
      <p className="mt-3">
        Don't have an account?{' '}
        <Link href="/signup">
          <a>Sign Up</a>
        </Link>
      </p>
      {/* <p className="mt-3">
        Forgot your Password? <Link href="/reset_password"><a>Reset Password</a></Link>
      </p> */}
    </>
  );
};
