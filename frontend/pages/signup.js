import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
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
    <Row className="justify-content-center">
      <Col md={8} lg={6}>
        <Card body>
          <h4 className="text-center">Sign Up</h4>
          <SignupForm signup={signup} />
          <p className="mt-3 text-center">
            Already have an account?{' '}
            <Link href="/login">
              <a>Login</a>
            </Link>
          </p>
        </Card>
      </Col>
    </Row>
  );
};
