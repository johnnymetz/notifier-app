import { useRouter } from 'next/router';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import SubmitButton from 'components/widgets/SubmitButton';
import useAuth from 'contexts/auth';

export default () => {
  const { isAuthenticated, login, error } = useAuth();
  const [username, setUsername] = React.useState(null);
  const [password, setPassword] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const router = useRouter();

  React.useEffect(() => {
    if (isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated]);

  const loginWrapper = async e => {
    e.preventDefault();
    if (username && password) {
      setLoading(true);
      await login(username, password);
      setLoading(false);
    }
  };

  return (
    <>
      <h2>Login</h2>
      <Form>
        <Form.Group>
          <Form.Label>Username</Form.Label>
          <Form.Control
            placeholder="Enter username"
            onChange={e => setUsername(e.target.value)}
          />
        </Form.Group>

        <Form.Group>
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter password"
            onChange={e => setPassword(e.target.value)}
          />
        </Form.Group>

        {error && <Alert variant={'danger'}>{error}</Alert>}

        <SubmitButton
          onClick={loginWrapper}
          isSubmitting={loading}
          variant="primary"
        >
          Submit
        </SubmitButton>
      </Form>
    </>
  );
};
