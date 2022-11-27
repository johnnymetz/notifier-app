import { useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';
import { toast } from 'react-toastify';

import useAuth from 'src/contexts/auth';
import apiClient from 'src/services/api';

const Layout = ({ children }) => {
  const { user, logout } = useAuth();

  const healthCheck = async () => {
    const { error } = await apiClient.getHealthCheck();
    console.log(error);
    if (error) {
      toast.error(`Can't connect to the backend: ${error}`);
    }
  };

  useEffect(() => {
    healthCheck();
  }, []);

  return (
    <>
      <Head>
        <title>Notifire</title>
        {getFavicon()}
      </Head>

      <Navbar bg="dark" variant="dark" expand="sm" className="mb-4">
        <Container>
          <Link href="/" legacyBehavior>
            <Navbar.Brand style={{ cursor: 'pointer' }}>
              <img src="/logo.png" alt="Notifire" height="40" />
            </Navbar.Brand>
          </Link>

          <Navbar.Toggle />
          <Navbar.Collapse className="justify-content-end">
            {!!user && (
              <Nav activeKey="">
                <Link href="/account" passHref legacyBehavior>
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

const getFavicon = () => (
  <>
    <link
      rel="apple-touch-icon"
      sizes="57x57"
      href="favicon/apple-icon-57x57.png"
    />
    <link
      rel="apple-touch-icon"
      sizes="60x60"
      href="favicon/apple-icon-60x60.png"
    />
    <link
      rel="apple-touch-icon"
      sizes="72x72"
      href="favicon/apple-icon-72x72.png"
    />
    <link
      rel="apple-touch-icon"
      sizes="76x76"
      href="favicon/apple-icon-76x76.png"
    />
    <link
      rel="apple-touch-icon"
      sizes="114x114"
      href="favicon/apple-icon-114x114.png"
    />
    <link
      rel="apple-touch-icon"
      sizes="120x120"
      href="favicon/apple-icon-120x120.png"
    />
    <link
      rel="apple-touch-icon"
      sizes="144x144"
      href="favicon/apple-icon-144x144.png"
    />
    <link
      rel="apple-touch-icon"
      sizes="152x152"
      href="favicon/apple-icon-152x152.png"
    />
    <link
      rel="apple-touch-icon"
      sizes="180x180"
      href="favicon/apple-icon-180x180.png"
    />
    <link
      rel="icon"
      type="image/png"
      sizes="192x192"
      href="favicon/android-icon-192x192.png"
    />
    <link
      rel="icon"
      type="image/png"
      sizes="32x32"
      href="favicon/favicon-32x32.png"
    />
    <link
      rel="icon"
      type="image/png"
      sizes="96x96"
      href="favicon/favicon-96x96.png"
    />
    <link
      rel="icon"
      type="image/png"
      sizes="16x16"
      href="favicon/favicon-16x16.png"
    />
    <link rel="manifest" href="favicon/manifest.json" />
    <meta name="msapplication-TileColor" content="#ffffff" />
    <meta
      name="msapplication-TileImage"
      content="favicon/ms-icon-144x144.png"
    />
    <meta name="theme-color" content="#ffffff" />
  </>
);

export default Layout;
