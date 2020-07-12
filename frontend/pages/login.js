import { useRouter } from 'next/router';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import Layout from 'components/Layout';
import { loginUser } from 'api';

export default () => {
  const [username, setUsername] = React.useState(null);
  const [password, setPassword] = React.useState(null);
  const [error, setError] = React.useState(null);
  const router = useRouter();

  const login = async e => {
    e.preventDefault();
    setError(null);
    if (username && password) {
      const { loggedIn, error } = await loginUser(username, password);
      if (loggedIn) {
        router.push('/');
      } else {
        setError(error);
      }
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

        <Button variant="primary" type="submit" onClick={login}>
          Submit
        </Button>
      </Form>
    </Layout>
  );
};
