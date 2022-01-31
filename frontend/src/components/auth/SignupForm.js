import { Formik, Form as FormikForm } from 'formik';
import Form from 'react-bootstrap/Form';

import { SignupSchema } from 'src/utils/formSchemas';
import TextField from 'src/components/widgets/formikFields/TextField';
import PasswordField from 'src/components/widgets/formikFields/PasswordField';
import SubmitButton from 'src/components/widgets/SubmitButton';

const SignupForm = ({ onSubmit }) => {
  return (
    <Formik
      initialValues={{ email: '', password: '', re_password: '' }}
      validationSchema={SignupSchema}
      onSubmit={async (values, { setFieldError }) => {
        await onSubmit(values, setFieldError);
      }}
    >
      {({ isSubmitting }) => (
        <FormikForm as={Form}>
          <TextField name="email" label="Email" dataTestId="signup-email" />

          <PasswordField
            name="password"
            label="Password"
            dataTestId="signup-password"
          />
          <PasswordField
            name="re_password"
            label="Verify Password"
            dataTestId="signup-re-password"
          />

          <SubmitButton isSubmitting={isSubmitting} variant="primary" block>
            Sign Up
          </SubmitButton>
        </FormikForm>
      )}
    </Formik>
  );
};

export default SignupForm;
