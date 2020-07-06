import Head from 'next/head';
import Link from 'next/link';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';

export default ({ children, home }) => {
  return (
    <div>
      <Head>
        <title>Notifier</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Navbar bg="dark" variant="dark" expand="sm" className="mb-3">
        <Container>
          <Link href="/">
            <Navbar.Brand href="#home">Notifier</Navbar.Brand>
          </Link>
          <Nav>
            <Nav.Link>Login</Nav.Link>
          </Nav>
        </Container>
      </Navbar>

      <Container>
        {children}
        {!home && (
          <Link href="/">
            <a>← Back to home</a>
          </Link>
        )}
      </Container>
    </div>
  );
};
