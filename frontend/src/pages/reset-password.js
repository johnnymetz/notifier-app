import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

import useAuth from 'src/contexts/auth';
import SendResetPasswordEmailForm from 'src/components/auth/SendResetPasswordEmailForm';

const ResetPassword = () => {
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
            <Link href="/login">Back to Login</Link>
          </p>
        </Card>
      </Col>
    </Row>
  );
};

export default ResetPassword;
