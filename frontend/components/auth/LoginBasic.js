import { useState } from 'react';
import { toast } from 'react-toastify';
import Form from 'react-bootstrap/Form';
import SubmitButton from 'components/widgets/SubmitButton';

export default ({ login }) => {
  const [email, setEmail] = useState(null);
  const [password, setPassword] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async e => {
    e.preventDefault();
    if (email && password) {
      setLoading(true);
      await login(email, password);
      setLoading(false);
    } else {
      toast.error('Email and password fields required');
    }
  };

  return (
    <Form>
      <Form.Group>
        <Form.Label>Email</Form.Label>
        <Form.Control
          placeholder="Enter email"
          onChange={e => setEmail(e.target.value)}
          data-test="email"
        />
      </Form.Group>

      <Form.Group>
        <Form.Label>Password</Form.Label>
        <Form.Control
          type="password"
          placeholder="Enter password"
          onChange={e => setPassword(e.target.value)}
          data-test="password"
        />
      </Form.Group>

      <SubmitButton
        onClick={handleSubmit}
        isSubmitting={loading}
        variant="primary"
      >
        Submit
      </SubmitButton>
    </Form>
  );
};
