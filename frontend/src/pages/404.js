import Link from 'next/link';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

const FourOhFour = () => {
  return (
    <Row className="justify-content-center">
      <Col sm={8}>
        <Card body className="text-center">
          <h1>404</h1>
          <p>Page Not Found</p>
          <div>
            <Link href="/">
              <a>Back to Home</a>
            </Link>
          </div>
        </Card>
      </Col>
    </Row>
  );
};

export default FourOhFour;
