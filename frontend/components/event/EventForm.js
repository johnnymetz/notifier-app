import { Formik, Form as FormikForm } from 'formik';
import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';

import apiClient from 'services/api';
import useAuth from 'contexts/auth';
import { EventSchema } from 'utils/formSchemas';
import { handleDrfError } from 'utils/helpers';
import TextField from 'components/widgets/formikFields/TextField';
import SelectField from 'components/widgets/formikFields/SelectField';
// import FormikDebug from 'components/widgets/formikFields/FormikDebug';
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

const EventForm = ({ action, eventValues, setShowModal }) => {
  const { fetchUser } = useAuth();
  const [eventTypeChoices, setEventTypeChoices] = useState(null);
  const [showMonthNames, setShowMonthNames] = useState(false);

  const currentDate = new Date();
  const currentMonth = currentDate.getMonth() + 1;
  const currentDay = currentDate.getDate();
  const monthOptions = MONTHS.map((m, i) => ({
    value: i + 1,
    label: showMonthNames ? m : (i + 1).toString().padStart(2, '0'),
  }));

  const getEventTypeChoices = async () => {
    const choices = await apiClient.getEventTypeChoices();
    if (choices) {
      const choicesTransformed = choices.map(x => ({
        value: x.value,
        label: x.display_name,
      }));
      setEventTypeChoices(choicesTransformed);
    }
  };

  useEffect(() => {
    getEventTypeChoices();
  }, []);

  const initialValues = {
    name: eventValues?.name || '',
    month: eventValues?.month || currentMonth,
    day: eventValues?.day || currentDay,
    year: eventValues?.year || '',
    type:
      eventValues?.type ||
      (eventTypeChoices && eventTypeChoices[0].value) ||
      '',
  };

  return (
    <Formik
      initialValues={initialValues}
      enableReinitialize={true} // reset the form if initialValues changes
      validationSchema={EventSchema}
      onSubmit={async (
        { name, month, day, year, type },
        { setSubmitting, setFieldError, resetForm }
      ) => {
        const payload = {
          name,
          annual_date: { month: parseInt(month), day: parseInt(day) },
          type,
        };
        if (year) {
          payload.annual_date.year = parseInt(year);
        }
        setSubmitting(true);
        let data, error;
        if (action === 'create') {
          ({ data, error } = await apiClient.createEvent(payload));
        } else if (action === 'update') {
          ({ data, error } = await apiClient.updateEvent(
            eventValues.id,
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
          handleDrfError(error, ['name', 'type'], setFieldError);
        }
        setSubmitting(false);
        if (setShowModal) {
          setShowModal(false);
        }
      }}
    >
      {({ isSubmitting }) => (
        <FormikForm as={Form} data-test={`${action}-event-form`}>
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
              options={monthOptions}
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

          {eventTypeChoices ? (
            <SelectField
              name="type"
              options={eventTypeChoices}
              label="Event Type"
              dataTestId={`${action}-event-type-input`}
            />
          ) : (
            <TextField
              name="type"
              label="Event Type"
              dataTestId={`${action}-event-type-input`}
            />
          )}

          <SubmitButton isSubmitting={isSubmitting} variant="primary" block>
            Submit
          </SubmitButton>
          {/* <FormikDebug /> */}
        </FormikForm>
      )}
    </Formik>
  );
};

export default EventForm;
