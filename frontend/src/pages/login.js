import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

import useAuth from 'src/contexts/auth';
import LoginForm from 'src/components/auth/LoginForm';

const Login = () => {
  const { user, login } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!!user) {
      router.push('/');
    }
  }, [user]);

  return (
    <Row className="justify-content-center">
      <Col md={8} lg={6}>
        <Card body>
          <h4 className="text-center">Login</h4>
          <LoginForm onSubmit={login} />
          <p className="mt-3 text-center">
            Don't have an account?{' '}
            <Link href="/signup" data-test="login-to-signup-link">
              Sign Up
            </Link>
          </p>
          <p className="mt-3 text-center">
            Forgot your Password?{' '}
            <Link href="/reset-password">Reset Password</Link>
          </p>
        </Card>
      </Col>
    </Row>
  );
};

export default Login;
