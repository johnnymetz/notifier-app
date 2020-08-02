import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import { toast } from 'react-toastify';
import SubmitButton from 'components/widgets/SubmitButton';
import useAuth from 'contexts/auth';
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

export default ({ requestMethod, friendValues = {}, setShowModal = null }) => {
  const { fetchUser } = useAuth();
  const [name, setName] = useState(friendValues.name || '');
  const [month, setMonth] = useState(friendValues.month || 1);
  const [day, setDay] = useState(friendValues.day || '');
  const [year, setYear] = useState(friendValues.year || '');
  const [loading, setLoading] = useState(false);

  const onSubmit = async e => {
    e.preventDefault();
    if (name && month && day) {
      const payload = {
        name: name,
        birthday_month: month,
        birthday_day: day,
      };
      if (year) {
        payload.birthday_year = year;
      }
      console.log(payload);
      setLoading(true);
      let data, error;
      if (requestMethod === 'POST') {
        ({ data, error } = await apiClient.authenticatedPost(
          'friends/',
          payload
        ));
      } else if (requestMethod === 'PATCH') {
        ({ data, error } = await apiClient.authenticatedPatch(
          `friends/${friendValues.id}/`,
          payload
        ));
      } else {
        throw Error(`Invalid request method: ${requestMethod}`);
      }
      if (data) {
        toast.success(
          `${name} successfully ${
            requestMethod === 'POST' ? 'added' : 'updated'
          }`
        );
        fetchUser();
        // TODO: uncomment eventually
        // setName('');
        // setMonth(1);
        // setDay('');
        // setYear('');
      } else {
        toast.error('Must fill out all required fields');
      }
      setLoading(false);
      if (setShowModal) {
        setShowModal(false);
      }
    } else {
      toast.error('Must fill out all required fields');
    }
  };

  return (
    <Form>
      <Form.Group>
        <Form.Label>Name *</Form.Label>
        <Form.Control
          // placeholder="Joe Maddon"
          value={name}
          onChange={e => setName(e.target.value)}
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
            // placeholder="24"
            value={day}
            onChange={e => setDay(e.target.value)}
          />
        </Form.Group>

        <Form.Group as={Col}>
          <Form.Label>Year</Form.Label>
          <Form.Control
            type="number"
            // placeholder="1994"
            value={year}
            onChange={e => setYear(e.target.value)}
          />
        </Form.Group>
      </Form.Row>

      <SubmitButton variant="primary" onClick={onSubmit} isSubmitting={loading}>
        Submit
      </SubmitButton>
    </Form>
  );
};
