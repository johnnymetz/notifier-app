import Head from 'next/head';
import Link from 'next/link';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';

import Favicon from 'components/widgets/Favicon';
import useAuth from 'contexts/auth';

export default ({ children }) => {
  const { user, logout } = useAuth();

  return (
    <>
      <Head>
        <title>Notifire</title>
        <Favicon />
      </Head>

      <Navbar bg="dark" variant="dark" expand="sm" className="mb-4">
        <Container>
          <Link href="/">
            <Navbar.Brand style={{ cursor: 'pointer' }}>
              <img src="/logo.png" alt="Notifire" height="40" />
            </Navbar.Brand>
          </Link>

          <Navbar.Toggle />
          <Navbar.Collapse className="justify-content-end">
            {!!user && (
              <Nav activeKey="">
                <Link href="/account" passHref>
                  <Nav.Link data-test="navbar-account-link">
                    <FontAwesomeIcon
                      icon={faUser}
                      size="sm"
                      style={{ marginRight: 5 }}
                    />{' '}
                    Account
                  </Nav.Link>
                </Link>
                <Nav.Link onClick={logout}>
                  <FontAwesomeIcon
                    icon={faSignOutAlt}
                    size="sm"
                    style={{ marginRight: 3 }}
                  />{' '}
                  Logout
                </Nav.Link>
              </Nav>
            )}
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container className="pb-4">{children}</Container>
    </>
  );
};
