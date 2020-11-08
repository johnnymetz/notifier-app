import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import useAuth from 'contexts/auth';
import SendResetPasswordEmailForm from 'components/auth/SendResetPasswordEmailForm';

export default () => {
  const { user, sendResetPasswordEmail } = useAuth();
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
          <h4 className="text-center">Reset Password</h4>
          <SendResetPasswordEmailForm onSubmit={sendResetPasswordEmail} />
          <p className="mt-3 text-center">
            <Link href="/login">
              <a>Back to Login</a>
            </Link>
          </p>
        </Card>
      </Col>
    </Row>
  );
};
