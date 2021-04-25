import { Formik, Form as FormikForm } from 'formik';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

import { SetEmailSchema } from 'utils/formSchemas';
import TextField from 'components/widgets/formikFields/TextField';
import PasswordField from 'components/widgets/formikFields/PasswordField';
import SubmitButton from 'components/widgets/SubmitButton';

const SetEmailForm = ({ onSubmit, setShowModal }) => {
  return (
    <Formik
      initialValues={{ new_email: '', re_new_email: '', current_password: '' }}
      validationSchema={SetEmailSchema}
      onSubmit={async (values, { setFieldError }) => {
        await onSubmit(values, setFieldError, setShowModal);
      }}
    >
      {({ isSubmitting }) => (
        <FormikForm as={Form}>
          <TextField
            name="new_email"
            label="Email"
            dataTestId="set-email-new-email"
          />
          <TextField
            name="re_new_email"
            label="Verify Email"
            dataTestId="set-email-re-new-email"
          />

          <PasswordField
            name="current_password"
            label="Password"
            dataTestId="set-email-current-password"
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

export default SetEmailForm;
