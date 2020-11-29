import { Formik, Form as FormikForm } from 'formik';
import Form from 'react-bootstrap/Form';

import { ResetPasswordSchema } from 'utils/formSchemas';
import PasswordField from 'components/widgets/formikFields/PasswordField';
import SubmitButton from 'components/widgets/SubmitButton';

export default ({ onSubmit, uid, token }) => {
  return (
    <Formik
      initialValues={{ new_password: '', re_new_password: '' }}
      validationSchema={ResetPasswordSchema}
      onSubmit={async (values, { setFieldError }) => {
        await onSubmit({ ...values, uid, token }, setFieldError);
      }}
    >
      {({ isSubmitting }) => (
        <FormikForm as={Form}>
          <PasswordField name="new_password" label="New Password" />
          <PasswordField name="re_new_password" label="Verify Password" />

          <SubmitButton isSubmitting={isSubmitting} variant="primary" block>
            Reset Password
          </SubmitButton>
        </FormikForm>
      )}
    </Formik>
  );
};
