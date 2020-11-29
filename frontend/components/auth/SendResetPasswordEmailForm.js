import { Formik, Form as FormikForm } from 'formik';
import Form from 'react-bootstrap/Form';

import { SendResetPasswordEmailSchema } from 'utils/formSchemas';
import TextField from 'components/widgets/formikFields/TextField';
import SubmitButton from 'components/widgets/SubmitButton';

export default ({ onSubmit }) => {
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
