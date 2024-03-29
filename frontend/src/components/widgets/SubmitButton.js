import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';

const SubmitButton = ({ onClick, isSubmitting, children, ...props }) => (
  <Button type="submit" onClick={onClick} disabled={isSubmitting} {...props}>
    {isSubmitting && <Spinner as="span" animation="border" size="sm" />}{' '}
    {children}
  </Button>
);

export default SubmitButton;
