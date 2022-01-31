import { Formik, Form as FormikForm } from 'formik';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

import { SetPasswordSchema } from 'src/utils/formSchemas';
import PasswordField from 'src/components/widgets/formikFields/PasswordField';
import SubmitButton from 'src/components/widgets/SubmitButton';

const SetPasswordForm = ({ onSubmit, setShowModal }) => {
  return (
    <Formik
      initialValues={{
        new_password: '',
        re_new_password: '',
        current_password: '',
      }}
      validationSchema={SetPasswordSchema}
      onSubmit={async (values, { setFieldError }) => {
        await onSubmit(values, setFieldError, setShowModal);
      }}
    >
      {({ isSubmitting }) => (
        <FormikForm as={Form}>
          <PasswordField
            name="new_password"
            label="New Password"
            dataTestId="set-password-new-password"
          />
          <PasswordField
            name="re_new_password"
            label="Verify New Password"
            dataTestId="set-password-re-new-password"
          />
          <PasswordField
            name="current_password"
            label="Current Password"
            dataTestId="set-password-current-password"
          />

          <SubmitButton isSubmitting={isSubmitting} variant="primary" block>
            Save Changes
          </SubmitButton>
          <Button onClick={() => setShowModal(false)} variant="light" block>
            Close
          </Button>
        </FormikForm>
      )}
    </Formik>
  );
};

export default SetPasswordForm;
