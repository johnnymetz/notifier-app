import { useState } from 'react';
import { useRouter } from 'next/router';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

import useAuth from 'src/contexts/auth';
import SubmitButton from 'src/components/widgets/SubmitButton';

const Activate = () => {
  const { activateUser } = useAuth();
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const activateUserWrapper = async () => {
    setIsSubmitting(true);
    await activateUser({ uid: router.query.uid, token: router.query.token });
    setIsSubmitting(false);
  };

  return (
    <Row className="justify-content-center">
      <Col md={8} lg={6}>
        <Card body className="text-center">
          <h3>Welcome!</h3>
          <div>Click the button below to activate your account.</div>
          <SubmitButton
            onClick={activateUserWrapper}
            isSubmitting={isSubmitting}
            variant="primary"
            className="mt-4"
          >
            Activate your account
          </SubmitButton>
        </Card>
      </Col>
    </Row>
  );
};

export default Activate;
