import { useState } from 'react';
import Link from 'next/link';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';

import SetEmailModal from 'src/components/auth/SetEmailModal';
import SetPasswordModal from 'src/components/auth/SetPasswordModal';
import { PrivateRoute, useAuth } from 'src/contexts/auth';

const AccountSetting = ({ label, value, onChange }) => (
  <ListGroup.Item>
    <div className="d-flex justify-content-between align-items-center">
      <div>
        <b>{label}</b>
        <div
          style={{ fontSize: '0.8rem' }}
          data-test={`account-${label.toLowerCase()}`}
        >
          {value}
        </div>
      </div>
      <a
        href="#"
        onClick={() => onChange(true)}
        data-test={`account-change-${label.toLowerCase()}`}
      >
        Change
      </a>
    </div>
  </ListGroup.Item>
);

const AccountSettingToggle = ({ label, field, value, onChange }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  return (
    <ListGroup.Item>
      <div className="d-flex justify-content-between align-items-center">
        <div>
          {label}{' '}
          {isSubmitting && <Spinner as="span" animation="border" size="sm" />}
        </div>
        <Form.Check
          type="checkbox"
          value={value}
          defaultChecked={value}
          onChange={async () => {
            setIsSubmitting(true);
            await onChange({ [field]: !value });
            setIsSubmitting(false);
          }}
          id={label.replace(/\s+/g, '-').toLowerCase()}
        />
      </div>
    </ListGroup.Item>
  );
};

const Account = () => {
  const { user, setEmail, setPassword, updateUser } = useAuth();
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
              <AccountSettingToggle
                label="Send me a daily morning email"
                field="is_subscribed"
                value={user.is_subscribed}
                onChange={updateUser}
              />
            </ListGroup>
            <div className="text-center mt-3">
              <Link href="/">Back to Home</Link>
            </div>
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
