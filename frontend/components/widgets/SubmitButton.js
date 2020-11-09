import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';

export default ({ onClick, isSubmitting, children, ...props }) => (
  <Button type="submit" onClick={onClick} disabled={isSubmitting} {...props}>
    {isSubmitting && <Spinner as="span" animation="border" size="sm" />}{' '}
    {children}
  </Button>
);
