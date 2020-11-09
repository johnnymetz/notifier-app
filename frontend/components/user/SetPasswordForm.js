import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { Formik, Form as FormikForm, Field, ErrorMessage } from 'formik';

import { SetPasswordSchema } from 'utils/formSchemas';
import SubmitButton from 'components/widgets/SubmitButton';

export default ({ onSubmit, setShowModal }) => {
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showReNewPassword, setShowReNewPassword] = useState(false);
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);

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
                data-test="set-password-new-password"
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
            <Form.Control.Feedback
              type="invalid"
              data-test="set-password-new-password-invalid-feedback"
            >
              <ErrorMessage name="new_password" />
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group>
            <Form.Label>Verify New Password</Form.Label>
            <InputGroup>
              <Field
                name="re_new_password"
                type={showReNewPassword ? 'text' : 'password'}
                as={Form.Control}
                isInvalid={touched.re_new_password && errors.re_new_password}
                data-test="set-password-re-new-password"
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
            <Form.Control.Feedback
              type="invalid"
              data-test="set-password-re-new-password-invalid-feedback"
            >
              <ErrorMessage name="re_new_password" />
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group>
            <Form.Label>Current Password</Form.Label>
            <InputGroup>
              <Field
                name="current_password"
                type={showCurrentPassword ? 'text' : 'password'}
                as={Form.Control}
                isInvalid={touched.current_password && errors.current_password}
                data-test="set-password-current-password"
              />
              <InputGroup.Append>
                <Button
                  variant="outline-secondary"
                  onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                  title={
                    showCurrentPassword ? 'Hide password' : 'Show password'
                  }
                >
                  <FontAwesomeIcon
                    icon={showCurrentPassword ? faEyeSlash : faEye}
                    size={'sm'}
                  />
                </Button>
              </InputGroup.Append>
            </InputGroup>
            <Form.Control.Feedback
              type="invalid"
              data-test="set-password-current-password-invalid-feedback"
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
