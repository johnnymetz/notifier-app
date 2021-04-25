import { useRouter } from 'next/router';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

import useAuth from 'contexts/auth';
import ResetPasswordForm from 'components/auth/ResetPasswordForm';

const PasswordResetConfirmation = () => {
  const { resetPassword } = useAuth();
  const router = useRouter();

  return (
    <Row className="justify-content-center">
      <Col md={8} lg={6}>
        <Card body>
          <h4 className="text-center">Reset Password</h4>
          <ResetPasswordForm
            onSubmit={resetPassword}
            uid={router.query.uid}
            token={router.query.token}
          />
        </Card>
      </Col>
    </Row>
  );
};

export default PasswordResetConfirmation;
