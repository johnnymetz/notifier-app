import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { Formik, Form as FormikForm, Field, ErrorMessage } from 'formik';

import { LoginSchema } from 'utils/formSchemas';
import SubmitButton from 'components/widgets/SubmitButton';
// import Debug from 'components/auth/FormikDebug';

export default ({ login }) => {
  const [showPassword, setShowPassword] = useState(false);
  const togglePasswordVisiblity = () => setShowPassword(!showPassword);

  return (
    <Formik
      initialValues={{ email: '', password: '' }}
      validationSchema={LoginSchema}
      onSubmit={async ({ email, password }) => {
        await login(email, password);
      }}
    >
      {({ errors, touched, isSubmitting }) => (
        <FormikForm as={Form}>
          <Form.Group>
            <Form.Label>Email</Form.Label>
            <Field
              name="email"
              placeholder="Enter email"
              as={Form.Control}
              // must have isInvalid to render invalid feedback
              // must have isValid to render valid feedback
              isInvalid={touched.email && errors.email}
              data-test="email"
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
                placeholder="Enter password"
                as={Form.Control}
                isInvalid={touched.password && errors.password}
                data-test="password"
              />
              <InputGroup.Append>
                <Button
                  variant="outline-secondary"
                  onClick={togglePasswordVisiblity}
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

          <SubmitButton isSubmitting={isSubmitting} variant="primary">
            Submit
          </SubmitButton>

          {/* <Debug /> */}
        </FormikForm>
      )}
    </Formik>
  );
};

/* <Form.Control
  name="email"
  value={values.name}
  placeholder="Enter email"
  onChange={handleChange}
  onBlur={handleBlur}
  isInvalid={!!errors.email}
  data-test="email"
/> */
/* {touched.email && errors.email && (
  <Form.Control.Feedback type="invalid">
    {errors.email}
  </Form.Control.Feedback>
)} */
