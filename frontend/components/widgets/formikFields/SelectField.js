import { useField } from 'formik';
import Form from 'react-bootstrap/Form';

export default ({
  name,
  options,
  label,
  labelProps,
  dataTestId,
  as,
  ...props
}) => {
  const [field, { touched, error }] = useField(name);

  return (
    <Form.Group as={as}>
      <Form.Label {...labelProps}>
        Month <span className="text-danger">&#x2a;</span>
      </Form.Label>
      <Form.Control
        name={name}
        as="select"
        isInvalid={touched && error}
        data-test={dataTestId}
        {...field}
        {...props}
      >
        {/* <option value="" disabled selected hidden>
              Month
            </option> */}
        {options}
      </Form.Control>
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
