import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';

import useAuth from 'contexts/auth';
import SignupForm from 'components/auth/SignupForm';

export default () => {
  const { isAuthenticated, signup } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated]);

  return (
    <>
      <h2>Sign Up</h2>
      <SignupForm signup={signup} />
      <p className="mt-3">
        Already have an account?{' '}
        <Link href="/login">
          <a>Login</a>
        </Link>
      </p>
    </>
  );
};
