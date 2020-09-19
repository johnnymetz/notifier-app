import { toast } from 'react-toastify';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import { Formik, Form as FormikForm, Field, ErrorMessage } from 'formik';

import apiClient from 'services/api';
import useAuth from 'contexts/auth';
import { FriendSchema } from 'utils/formSchemas';
import SubmitButton from 'components/widgets/SubmitButton';
// import Debug from 'components/auth/FormikDebug';

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

export default ({ action, friendValues = {}, setShowModal = null }) => {
  const { fetchUser } = useAuth();

  return (
    <Formik
      initialValues={{ name: '', month: 1, day: '', year: '' }}
      validationSchema={FriendSchema}
      onSubmit={async (
        { name, month, day, year },
        { setSubmitting, setFieldError }
      ) => {
        const payload = {
          name: name,
          date_of_birth: { month: parseInt(month), day: parseInt(day) },
        };
        if (year) {
          payload.date_of_birth.year = parseInt(year);
        }
        // console.log(payload);
        setSubmitting(true);
        let data, error;
        if (action === 'create') {
          ({ data, error } = await apiClient.authenticatedPost(
            'friends/',
            payload
          ));
        } else if (action === 'update') {
          ({ data, error } = await apiClient.authenticatedPatch(
            `friends/${friendValues.id}/`,
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
          // TODO: reset form fields eventually
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
      {({
        values,
        errors,
        touched,
        handleChange,
        handleBlur,
        isSubmitting,
      }) => (
        <FormikForm as={Form}>
          <Form.Group>
            <Form.Label>Name *</Form.Label>
            <Field
              name="name"
              as={Form.Control}
              isInvalid={touched.name && errors.name}
              data-test={`${action}-name-input`}
            />
            <Form.Control.Feedback type="invalid">
              <ErrorMessage name="name" />
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Row>
            <Form.Group as={Col}>
              <Form.Label>Month *</Form.Label>
              <Form.Control
                name="month"
                as="select"
                placeholder="Monthy"
                value={values.month}
                onChange={handleChange}
                onBlur={handleBlur}
                isInvalid={touched.month && errors.month}
                data-test={`${action}-month-input`}
              >
                {/* <option value="" disabled selected hidden>
                  Month
                </option> */}
                {MONTHS.map((m, i) => (
                  <option key={i} value={i + 1}>
                    {m}
                  </option>
                ))}
              </Form.Control>
              <Form.Control.Feedback type="invalid">
                <ErrorMessage name="month" />
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group as={Col}>
              <Form.Label>Day *</Form.Label>
              <Field
                type="number"
                name="day"
                as={Form.Control}
                isInvalid={touched.day && errors.day}
                data-test={`${action}-day-input`}
              />
              <Form.Control.Feedback type="invalid">
                <ErrorMessage name="day" />
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group as={Col}>
              <Form.Label>Year</Form.Label>
              <Field
                type="number"
                name="year"
                as={Form.Control}
                isInvalid={touched.year && errors.year}
                data-test={`${action}-year-input`}
              />
              <Form.Control.Feedback type="invalid">
                <ErrorMessage name="year" />
              </Form.Control.Feedback>
            </Form.Group>
          </Form.Row>

          <SubmitButton isSubmitting={isSubmitting} variant="primary">
            Submit
          </SubmitButton>

          {/* <Debug /> */}
        </FormikForm>
      )}
    </Formik>
  );
};
