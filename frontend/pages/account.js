import { useState } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import SetEmailModal from 'components/user/SetEmailModal';
import SetPasswordModal from 'components/user/SetPasswordModal';
import { PrivateRoute, useAuth } from 'contexts/auth';

const AccountSetting = ({ label, value, onChange }) => (
  <ListGroup.Item>
    <div className="d-flex justify-content-between align-items-center">
      <div>
        <b>{label}</b>
        <div style={{ fontSize: '0.8rem' }}>{value}</div>
      </div>
      <a href="#" onClick={() => onChange(true)}>
        Change
      </a>
    </div>
  </ListGroup.Item>
);

const Account = () => {
  const { user, setEmail, setPassword } = useAuth();
  const [showSetEmailModal, setShowSetEmailModal] = useState(false);
  const [showSetPasswordModal, setShowSetPasswordModal] = useState(false);

  return (
    <>
      <Row className="justify-content-center">
        <Col sm={8}>
          <Card body>
            <h5 className="text-center">Account Settings</h5>
            <ListGroup>
              <AccountSetting
                label="Email"
                value={user.email}
                onChange={setShowSetEmailModal}
              />
              <AccountSetting
                label="Password"
                value={<span className="text-muted">********</span>}
                onChange={setShowSetPasswordModal}
              />
            </ListGroup>
          </Card>
        </Col>
      </Row>

      <SetEmailModal
        showModal={showSetEmailModal}
        setShowModal={setShowSetEmailModal}
        onSubmit={setEmail}
      />

      <SetPasswordModal
        showModal={showSetPasswordModal}
        setShowModal={setShowSetPasswordModal}
        onSubmit={setPassword}
      />
    </>
  );
};

export default PrivateRoute(Account);
