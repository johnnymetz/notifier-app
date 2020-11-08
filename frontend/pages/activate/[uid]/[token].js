import { useState } from 'react';
import { useRouter } from 'next/router';

import useAuth from 'contexts/auth';
import SubmitButton from 'components/widgets/SubmitButton';

export default () => {
  const { activateUser } = useAuth();
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const activateUserWrapper = async () => {
    setIsSubmitting(true);
    await activateUser({ uid: router.query.uid, token: router.query.token });
    setIsSubmitting(false);
  };

  return (
    <div className="d-flex flex-column justify-content-center align-items-center">
      <h2>Welcome!</h2>
      <div>Click the button below to activate your account.</div>
      <SubmitButton
        onClick={activateUserWrapper}
        isSubmitting={isSubmitting}
        variant="primary"
        className="mt-4"
      >
        Activate your account
      </SubmitButton>
    </div>
  );
};
