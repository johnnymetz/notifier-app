import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Alert from 'react-bootstrap/Alert';
import SubmitButton from 'components/widgets/SubmitButton';
import apiClient from 'services/api';
import useAuth from 'contexts/auth';

const MONTHS = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
];
// UNKOWN_YEAR = 1000;

export default () => {
  const { fetchUser } = useAuth();
  const [firstName, setFirstName] = React.useState('');
  const [lastName, setLastName] = React.useState('');
  const [month, setMonth] = React.useState(1);
  const [day, setDay] = React.useState('');
  const [year, setYear] = React.useState('');
  const [loading, setLoading] = React.useState(null);
  const [alertMessage, setAlertMessage] = React.useState(null);
  const [alertVariant, setAlertVariant] = React.useState(null);

  const onSubmit = async e => {
    e.preventDefault();
    setAlertMessage(null);
    setAlertVariant(null);
    if (firstName && month && day) {
      const payload = {
        first_name: firstName,
        // 'birthday': `${year || UNKOWN_YEAR}-${month}-${day}`
        birthday: year
          ? `${year}-${month
              .toString()
              .padStart(2, 0)}-${day.toString().padStart(2, 0)}`
          : `${month.toString().padStart(2, 0)}-${day
              .toString()
              .padStart(2, 0)}`,
      };
      if (lastName) {
        payload.last_name = lastName;
      }
      console.log(payload);
      setLoading(true);
      const { data, error } = await apiClient.authenticatedPost(
        'friends/',
        payload
      );
      if (data) {
        setAlertMessage(`${firstName} ${lastName} successfully added`);
        setAlertVariant('success');
        fetchUser();
      } else {
        setAlertMessage(error);
        setAlertVariant('danger');
      }
      setLoading(false);
      setFirstName('');
      setLastName('');
      setMonth(1);
      setDay('');
      setYear('');
    } else {
      setAlertMessage('Must fill out all required fields');
      setAlertVariant('danger');
    }
  };

  return (
    <div>
      <h4>Add Friend</h4>
      <Form>
        <Form.Group>
          <Form.Label>First Name *</Form.Label>
          <Form.Control
            placeholder="Joe"
            value={firstName}
            onChange={e => setFirstName(e.target.value)}
          />
        </Form.Group>

        <Form.Group>
          <Form.Label>Last Name</Form.Label>
          <Form.Control
            placeholder="Maddon"
            value={lastName}
            onChange={e => setLastName(e.target.value)}
          />
        </Form.Group>

        <Form.Row>
          <Form.Group as={Col}>
            <Form.Label>Month *</Form.Label>
            <Form.Control
              as="select"
              value={month}
              onChange={e => setMonth(e.target.value)}
            >
              {MONTHS.map((m, i) => (
                <option key={i} value={i + 1}>
                  {m}
                </option>
              ))}
            </Form.Control>
          </Form.Group>

          <Form.Group as={Col}>
            <Form.Label>Day *</Form.Label>
            <Form.Control
              type="number"
              placeholder="24"
              value={day}
              onChange={e => setDay(e.target.value)}
            />
          </Form.Group>

          <Form.Group as={Col}>
            <Form.Label>Year</Form.Label>
            <Form.Control
              type="number"
              placeholder="1994"
              value={year}
              onChange={e => setYear(e.target.value)}
            />
          </Form.Group>
        </Form.Row>

        {alertMessage && <Alert variant={alertVariant}>{alertMessage}</Alert>}

        <SubmitButton
          variant="primary"
          onClick={onSubmit}
          isSubmitting={loading}
        >
          Submit
        </SubmitButton>
      </Form>
    </div>
  );
};
