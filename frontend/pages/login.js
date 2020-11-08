import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
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
    <Row className="justify-content-center">
      <Col md={8} lg={6}>
        <Card body>
          <h4 className="text-center">Login</h4>
          <LoginForm login={login} />
          <p className="mt-3 text-center">
            Don't have an account?{' '}
            <Link href="/signup">
              <a>Sign Up</a>
            </Link>
          </p>
          {/* <p className="mt-3 text-center">
            Forgot your Password? <Link href="/reset_password"><a>Reset Password</a></Link>
          </p> */}
        </Card>
      </Col>
    </Row>
  );
};
