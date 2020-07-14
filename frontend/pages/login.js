import { useRouter } from 'next/router';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import Layout from 'components/Layout';
import SubmitButton from 'components/widgets/SubmitButton';
import useAuth from 'contexts/auth';

export default () => {
  const [username, setUsername] = React.useState(null);
  const [password, setPassword] = React.useState(null);
  const router = useRouter();
  const { isAuthenticated, login, loading, error } = useAuth();

  React.useEffect(() => {
    if (isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated]);

  const loginWithCreds = async e => {
    e.preventDefault();
    if (username && password) {
      await login(username, password);
    }
  };

  return (
    <Layout>
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
          onClick={loginWithCreds}
          isSubmitting={loading}
          variant="primary"
        >
          Submit
        </SubmitButton>
      </Form>
    </Layout>
  );
};
