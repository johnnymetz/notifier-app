import Head from 'next/head';
import Link from 'next/link';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Favicon from 'components/widgets/Favicon';
import useAuth from 'contexts/auth';

export default ({ children }) => {
  const { isAuthenticated, logout } = useAuth();

  return (
    <div>
      <Head>
        <title>Notifire</title>
        <Favicon />
      </Head>

      <Navbar bg="dark" variant="dark" expand="sm" className="mb-3">
        <Container>
          <Link href="/">
            <Navbar.Brand style={{ cursor: 'pointer' }}>
              <img src="/logo.png" alt="Notifire" height="40" />
            </Navbar.Brand>
          </Link>
          <Navbar.Toggle />
          <Navbar.Collapse className="justify-content-end">
            {isAuthenticated && (
              <Nav>
                <Nav.Link onClick={logout}>Logout</Nav.Link>
              </Nav>
            )}
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container>{children}</Container>
    </div>
  );
};
