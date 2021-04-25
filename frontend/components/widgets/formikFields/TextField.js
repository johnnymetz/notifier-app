import { useField } from 'formik';
import Form from 'react-bootstrap/Form';

const TextField = ({ name, label, dataTestId, as, ...props }) => {
  const [field, { touched, error }] = useField(name);

  return (
    <Form.Group as={as}>
      <Form.Label>{label}</Form.Label>
      <Form.Control
        name={name}
        // must have isInvalid to render invalid feedback
        // must have isValid to render valid feedback
        // (not anymore because we're setting .invalid-feedback to block display in global css)
        isInvalid={touched && error}
        data-test={dataTestId}
        {...field}
        {...props}
      />
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

export default TextField;
