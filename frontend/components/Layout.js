import Head from 'next/head';
import Link from 'next/link';
// import { useRouter } from 'next/router';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
// import Nav from 'react-bootstrap/Nav';
// import { verifyToken, logoutUser } from 'api';

export default ({ children, home }) => {
  // const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  // const router = useRouter();

  // React.useEffect(() => {
  //   const verified = verifyToken();
  //   if (verified) {
  //     setIsLoggedIn(true);
  //   }
  // }, []);

  // const logout = () => {
  //   logoutUser();
  //   router.push('/login');
  // };

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
          {/* {isLoggedIn && (
            <Nav>
              <Nav.Link onClick={logout}>Logout</Nav.Link>
            </Nav>
          )} */}
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
