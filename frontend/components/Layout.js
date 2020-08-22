import Head from 'next/head';
import Link from 'next/link';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import Favicon from 'components/widgets/Favicon';
import useAuth from 'contexts/auth';

export default ({ children, home }) => {
  const { isAuthenticated, logout } = useAuth();

  return (
    <div>
      <Head>
        <title>Notifier</title>
        <Favicon />
      </Head>

      <Navbar bg="dark" variant="dark" expand="sm" className="mb-3">
        <Container>
          <Link href="/">
            <Navbar.Brand style={{ cursor: 'pointer' }}>
              <FontAwesomeIcon icon={faPaperPlane} size={'sm'} />
              <span style={{ marginLeft: 8 }}>Notifier</span>
              {/* <img src="/logo.png" alt="Notifier" height="40" /> */}
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

      <Container>
        {children}
        {/* {!home && (
          <div>
            <Link href="/">
              <a>← Back to home</a>
            </Link>
          </div>
        )} */}
      </Container>
    </div>
  );
};
