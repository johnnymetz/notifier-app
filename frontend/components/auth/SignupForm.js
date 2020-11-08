import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { Formik, Form as FormikForm, Field, ErrorMessage } from 'formik';

import { SignupSchema } from 'utils/formSchemas';
import SubmitButton from 'components/widgets/SubmitButton';
// import Debug from 'components/auth/FormikDebug';

export default ({ onSubmit }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [showRePassword, setShowRePassword] = useState(false);

  return (
    <Formik
      initialValues={{ email: '', password: '', re_password: '' }}
      validationSchema={SignupSchema}
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

          <Form.Group>
            <Form.Label>Password</Form.Label>
            <InputGroup>
              <Field
                name="password"
                type={showPassword ? 'text' : 'password'}
                as={Form.Control}
                isInvalid={touched.password && errors.password}
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
            <Form.Control.Feedback type="invalid">
              <ErrorMessage name="password" />
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group>
            <Form.Label>Verify Password</Form.Label>
            <InputGroup>
              <Field
                name="re_password"
                type={showRePassword ? 'text' : 'password'}
                as={Form.Control}
                isInvalid={touched.re_password && errors.re_password}
              />
              <InputGroup.Append>
                <Button
                  variant="outline-secondary"
                  onClick={() => setShowRePassword(!showRePassword)}
                  title={showRePassword ? 'Hide password' : 'Show password'}
                >
                  <FontAwesomeIcon
                    icon={showRePassword ? faEyeSlash : faEye}
                    size={'sm'}
                  />
                </Button>
              </InputGroup.Append>
            </InputGroup>
            <Form.Control.Feedback type="invalid">
              <ErrorMessage name="re_password" />
            </Form.Control.Feedback>
          </Form.Group>

          <SubmitButton isSubmitting={isSubmitting} variant="primary" block>
            Signup
          </SubmitButton>

          {/* <Debug /> */}
        </FormikForm>
      )}
    </Formik>
  );
};
