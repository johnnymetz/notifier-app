import { Formik, Form as FormikForm } from 'formik';
import { useState } from 'react';
import { toast } from 'react-toastify';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';

import apiClient from 'services/api';
import useAuth from 'contexts/auth';
import { range, padNumber } from 'utils/helpers';
import { EventSchema } from 'utils/formSchemas';
import TextField from 'components/widgets/formikFields/TextField';
import SelectField from 'components/widgets/formikFields/SelectField';
import SubmitButton from 'components/widgets/SubmitButton';

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

export default ({ action, eventValues = {}, setShowModal = null }) => {
  const { fetchUser } = useAuth();
  const [showMonthNames, setShowMonthNames] = useState(false);

  const initialValues = {
    name: eventValues.name || '',
    month: eventValues.month || 1,
    day: eventValues.day || '',
    year: eventValues.year || '',
  };

  const getMonthDropdownOptions = () => {
    let options = [];
    if (showMonthNames) {
      MONTHS.map((m, i) => {
        options.push(
          <option key={i} value={i + 1}>
            {m}
          </option>
        );
      });
    } else {
      range(1, 13).map(i => {
        options.push(
          <option key={i} value={i}>
            {padNumber(i)}
          </option>
        );
      });
    }
    return options;
  };

  return (
    <Formik
      initialValues={initialValues}
      validationSchema={EventSchema}
      onSubmit={async (
        { name, month, day, year },
        { setSubmitting, setFieldError, resetForm }
      ) => {
        const payload = {
          name: name,
          annual_date: { month: parseInt(month), day: parseInt(day) },
        };
        if (year) {
          payload.annual_date.year = parseInt(year);
        }
        setSubmitting(true);
        let data, error;
        if (action === 'create') {
          ({ data, error } = await apiClient.authenticatedPost(
            'events/',
            payload
          ));
        } else if (action === 'update') {
          ({ data, error } = await apiClient.authenticatedPatch(
            `events/${eventValues.id}/`,
            payload
          ));
        } else {
          throw Error(`Invalid action: ${action}`);
        }
        if (data) {
          toast.success(
            `"${name}" successfully ${
              action === 'create' ? 'added' : 'updated'
            }`
          );
          fetchUser();
          resetForm();
        } else {
          console.warn(error);
          if (error.name) {
            setFieldError('name', error.name[0]);
          } else if (typeof error === 'string') {
            toast.error(error);
          }
        }
        setSubmitting(false);
        if (setShowModal) {
          setShowModal(false);
        }
      }}
    >
      {({ isSubmitting }) => (
        <FormikForm as={Form}>
          <TextField
            name="name"
            label={
              <span>
                Name <span className="text-danger">&#x2a;</span>
              </span>
            }
            dataTestId={`${action}-event-name-input`}
          />

          <Form.Row>
            <SelectField
              name="month"
              options={getMonthDropdownOptions()}
              label={
                <span>
                  Month <span className="text-danger">&#x2a;</span>
                </span>
              }
              labelProps={{
                title: 'Click to toggle month names',
                onClick: () => setShowMonthNames(!showMonthNames),
              }}
              dataTestId={`${action}-event-month-input`}
              as={Col}
            />

            <TextField
              name="day"
              label={
                <span>
                  Day <span className="text-danger">&#x2a;</span>
                </span>
              }
              dataTestId={`${action}-event-day-input`}
              type="number"
              as={Col}
            />

            <TextField
              name="year"
              label="Year"
              dataTestId={`${action}-event-year-input`}
              type="number"
              as={Col}
            />
          </Form.Row>

          <SubmitButton isSubmitting={isSubmitting} variant="primary" block>
            Submit
          </SubmitButton>
        </FormikForm>
      )}
    </Formik>
  );
};