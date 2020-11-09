import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

import useAuth from 'contexts/auth';
import SignupForm from 'components/auth/SignupForm';

export default () => {
  const { user, createUser } = useAuth();
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
          <h4 className="text-center">Sign Up</h4>
          <SignupForm onSubmit={createUser} />
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
