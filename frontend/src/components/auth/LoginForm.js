import { Formik, Form as FormikForm } from 'formik';
import Form from 'react-bootstrap/Form';

import { LoginSchema } from 'src/utils/formSchemas';
import TextField from 'src/components/widgets/formikFields/TextField';
import PasswordField from 'src/components/widgets/formikFields/PasswordField';
import SubmitButton from 'src/components/widgets/SubmitButton';

const LoginForm = ({ onSubmit }) => {
  return (
    <Formik
      initialValues={{ email: '', password: '' }}
      validationSchema={LoginSchema}
      onSubmit={async (values, { setFieldError }) => {
        await onSubmit(values, setFieldError);
      }}
    >
      {({ isSubmitting }) => (
        <FormikForm as={Form}>
          <TextField name="email" label="Email" dataTestId="login-email" />

          <PasswordField
            name="password"
            label="Password"
            dataTestId="login-password"
          />

          <SubmitButton isSubmitting={isSubmitting} variant="primary" block>
            Continue
          </SubmitButton>
        </FormikForm>
      )}
    </Formik>
  );
};

export default LoginForm;
