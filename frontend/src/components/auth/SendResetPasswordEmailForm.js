import { Formik, Form as FormikForm } from 'formik';
import Form from 'react-bootstrap/Form';

import { SendResetPasswordEmailSchema } from 'src/utils/formSchemas';
import TextField from 'src/components/widgets/formikFields/TextField';
import SubmitButton from 'src/components/widgets/SubmitButton';

const SendResetPasswordEmailForm = ({ onSubmit }) => {
  return (
    <Formik
      initialValues={{ email: '' }}
      validationSchema={SendResetPasswordEmailSchema}
      onSubmit={async (values, { setFieldError }) => {
        await onSubmit(values, setFieldError);
      }}
    >
      {({ isSubmitting }) => (
        <FormikForm as={Form}>
          <TextField name="email" label="Email" />

          <SubmitButton isSubmitting={isSubmitting} variant="primary" block>
            Reset Password
          </SubmitButton>
        </FormikForm>
      )}
    </Formik>
  );
};

export default SendResetPasswordEmailForm;
