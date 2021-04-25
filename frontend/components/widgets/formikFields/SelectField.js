import { useField } from 'formik';
import Form from 'react-bootstrap/Form';

const SelectField = ({
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
      <Form.Label {...labelProps}>{label}</Form.Label>
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
        {options.map((x, i) => (
          <option key={i} value={x.value}>
            {x.label}
          </option>
        ))}
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

export default SelectField;
