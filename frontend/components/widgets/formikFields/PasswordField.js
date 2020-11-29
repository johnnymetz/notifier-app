import { useField } from 'formik';
import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';

export default ({ name, label, dataTestId, ...props }) => {
  const [field, { touched, error }] = useField(name);
  const [showPassword, setShowPassword] = useState(false);

  return (
    <Form.Group>
      <Form.Label>{label}</Form.Label>
      <InputGroup>
        <Form.Control
          name={name}
          type={showPassword ? 'text' : 'password'}
          isInvalid={touched && error}
          data-test={dataTestId}
          style={{ borderRight: (!touched || !error) && 0 }}
          {...field}
          {...props}
        />
        <InputGroup.Append>
          <Button
            variant="link"
            onClick={() => setShowPassword(!showPassword)}
            title={showPassword ? 'Hide password' : 'Show password'}
            style={{ border: '1px solid #ced4da', borderLeft: 0 }}
          >
            <FontAwesomeIcon
              icon={showPassword ? faEyeSlash : faEye}
              size={'sm'}
            />
          </Button>
        </InputGroup.Append>
      </InputGroup>
      {touched && error && (
        <Form.Control.Feedback
          type="invalid"
          data-test={dataTestId && `${dataTestId}-invalid-feedback`}
        >
          {error}
        </Form.Control.Feedback>
      )}
    </Form.Group>
  );
};
