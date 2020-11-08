import Form from 'react-bootstrap/Form';
import { Formik, Form as FormikForm, Field, ErrorMessage } from 'formik';

import { SendResetPasswordEmailSchema } from 'utils/formSchemas';
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
      {({ errors, touched, isSubmitting }) => (
        <FormikForm as={Form}>
          <Form.Group>
            <Form.Label>Email</Form.Label>
            <Field
              name="email"
              as={Form.Control}
              isInvalid={touched.email && errors.email}
            />
            <Form.Control.Feedback type="invalid">
              <ErrorMessage name="email" />
            </Form.Control.Feedback>
          </Form.Group>

          <SubmitButton isSubmitting={isSubmitting} variant="primary" block>
            Reset Password
          </SubmitButton>
        </FormikForm>
      )}
    </Formik>
  );
};
