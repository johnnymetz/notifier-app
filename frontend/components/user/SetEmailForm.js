import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { Formik, Form as FormikForm, Field, ErrorMessage } from 'formik';

import { SetEmailSchema } from 'utils/formSchemas';
import SubmitButton from 'components/widgets/SubmitButton';

export default ({ onSubmit, setShowModal }) => {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <Formik
      initialValues={{ new_email: '', re_new_email: '', current_password: '' }}
      validationSchema={SetEmailSchema}
      onSubmit={async (values, { setFieldError }) => {
        await onSubmit(values, setFieldError, setShowModal);
      }}
    >
      {({ errors, touched, isSubmitting }) => (
        <FormikForm as={Form}>
          <Form.Group>
            <Form.Label>Email</Form.Label>
            <Field
              name="new_email"
              as={Form.Control}
              isInvalid={touched.new_email && errors.new_email}
              data-test="set-email-new-email"
            />
            <Form.Control.Feedback
              type="invalid"
              data-test="set-email-new-email-invalid-feedback"
            >
              <ErrorMessage name="new_email" />
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group>
            <Form.Label>Verify Email</Form.Label>
            <Field
              name="re_new_email"
              as={Form.Control}
              isInvalid={touched.re_new_email && errors.re_new_email}
              data-test="set-email-re-new-email"
            />
            <Form.Control.Feedback
              type="invalid"
              data-test="set-email-re-new-email-invalid-feedback"
            >
              <ErrorMessage name="re_new_email" />
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group>
            <Form.Label>Password</Form.Label>
            <InputGroup>
              <Field
                name="current_password"
                type={showPassword ? 'text' : 'password'}
                as={Form.Control}
                isInvalid={touched.current_password && errors.current_password}
                data-test="set-email-current-password"
              />
              <InputGroup.Append>
                <Button
                  variant="outline-secondary"
                  onClick={() => setShowPassword(!showPassword)}
                  title={showPassword ? 'Hide password' : 'Show password'}
                >
                  <FontAwesomeIcon
                    icon={showPassword ? faEyeSlash : faEye}
                    size={'sm'}
                  />
                </Button>
              </InputGroup.Append>
            </InputGroup>
            <Form.Control.Feedback
              type="invalid"
              data-test="set-email-current-password-invalid-feedback"
            >
              <ErrorMessage name="current_password" />
            </Form.Control.Feedback>
          </Form.Group>

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
