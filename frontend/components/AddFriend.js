import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Alert from 'react-bootstrap/Alert';
import SubmitButton from 'components/widgets/SubmitButton';
import apiClient from 'services/api';

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
  const [firstName, setFirstName] = React.useState(null);
  const [lastName, setLastName] = React.useState(null);
  const [month, setMonth] = React.useState(null);
  const [day, setDay] = React.useState(null);
  const [year, setYear] = React.useState(null);
  const [loading, setLoading] = React.useState(null);
  const [alertMessage, setAlertMessage] = React.useState(null);
  const [alertVariant, setAlertVariant] = React.useState(null);

  const onSubmit = async e => {
    e.preventDefault();
    const payload = {
      first_name: firstName,
      last_name: lastName,
      // 'birthday': `${year || UNKOWN_YEAR}-${month}-${day}`
      birthday: year
        ? `${year}-${month.padStart(2, 0)}-${day.padStart(2, 0)}`
        : `${month.padStart(2, 0)}-${day.padStart(2, 0)}`,
    };
    console.log(payload);
    // setLoading(true);
    // const { data, error } = await apiClient.authenticatedPost(
    //   'friends/',
    //   payload
    // );
    // console.log(data);
    // console.log(error);
    // if (data) {
    //   setAlertMessage(`${firstName} ${lastName} successfully added`);
    //   setAlertVariant('success');
    // } else {
    //   setAlertMessage(error);
    //   setAlertVariant('danger');
    // }
    // setLoading(false);
    // for (const setter in [setFirstName, setLastName, setMonth, setDay]) {
    //   setter(null);
    // }
  };

  return (
    <div>
      <h4>Add Friend</h4>
      <Form>
        <Form.Group>
          <Form.Label>First Name *</Form.Label>
          <Form.Control
            placeholder="Joe"
            onChange={e => setFirstName(e.target.value)}
          />
        </Form.Group>

        <Form.Group>
          <Form.Label>Last Name *</Form.Label>
          <Form.Control
            placeholder="Maddon"
            onChange={e => setLastName(e.target.value)}
          />
        </Form.Group>

        <Form.Row>
          <Form.Group as={Col}>
            <Form.Label>Month *</Form.Label>
            <Form.Control as="select" onChange={e => setMonth(e.target.value)}>
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
              placeholder="24"
              onChange={e => setDay(e.target.value)}
            />
          </Form.Group>

          <Form.Group as={Col}>
            <Form.Label>Year</Form.Label>
            <Form.Control
              placeholder="1994"
              onChange={e => setYear(e.target.value)}
            />
          </Form.Group>
        </Form.Row>

        {alertMessage && <Alert variant={alertVariant}>{alertMessage}</Alert>}

        <SubmitButton
          onClick={onSubmit}
          isSubmitting={loading}
          variant="primary"
        >
          Submit
        </SubmitButton>
      </Form>
    </div>
  );
};
