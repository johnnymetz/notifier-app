import Head from 'next/head';
import Container from 'react-bootstrap/Container';
import Link from 'next/link';

export default ({ children, home }) => {
  return (
    <div>
      <Head>
        <title>Notifier</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container>
        <h2>Notifier App</h2>
        <hr />

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
