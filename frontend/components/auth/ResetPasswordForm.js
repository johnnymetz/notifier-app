import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { Formik, Form as FormikForm, Field, ErrorMessage } from 'formik';

import { ResetPasswordSchema } from 'utils/formSchemas';
import SubmitButton from 'components/widgets/SubmitButton';

export default ({ onSubmit, uid, token }) => {
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showReNewPassword, setShowReNewPassword] = useState(false);

  return (
    <Formik
      initialValues={{ new_password: '', re_new_password: '' }}
      validationSchema={ResetPasswordSchema}
      onSubmit={async (values, { setFieldError }) => {
        await onSubmit({ ...values, uid, token }, setFieldError);
      }}
    >
      {({ errors, touched, isSubmitting }) => (
        <FormikForm as={Form}>
          <Form.Group>
            <Form.Label>New Password</Form.Label>
            <InputGroup>
              <Field
                name="new_password"
                type={showNewPassword ? 'text' : 'password'}
                as={Form.Control}
                isInvalid={touched.new_password && errors.new_password}
              />
              <InputGroup.Append>
                <Button
                  variant="outline-secondary"
                  onClick={() => setShowNewPassword(!showNewPassword)}
                  title={showNewPassword ? 'Hide password' : 'Show password'}
                >
                  <FontAwesomeIcon
                    icon={showNewPassword ? faEyeSlash : faEye}
                    size={'sm'}
                  />
                </Button>
              </InputGroup.Append>
            </InputGroup>
            <Form.Control.Feedback type="invalid">
              <ErrorMessage name="new_password" />
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group>
            <Form.Label>Verify Password</Form.Label>
            <InputGroup>
              <Field
                name="re_new_password"
                type={showReNewPassword ? 'text' : 'password'}
                as={Form.Control}
                isInvalid={touched.re_new_password && errors.re_new_password}
              />
              <InputGroup.Append>
                <Button
                  variant="outline-secondary"
                  onClick={() => setShowReNewPassword(!showReNewPassword)}
                  title={showReNewPassword ? 'Hide password' : 'Show password'}
                >
                  <FontAwesomeIcon
                    icon={showReNewPassword ? faEyeSlash : faEye}
                    size={'sm'}
                  />
                </Button>
              </InputGroup.Append>
            </InputGroup>
            <Form.Control.Feedback type="invalid">
              <ErrorMessage name="re_new_password" />
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
