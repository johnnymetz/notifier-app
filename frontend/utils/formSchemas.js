import * as Yup from 'yup';

export const FriendSchema = Yup.object().shape({
  name: Yup.string().required('Required'),
  day: Yup.number().required('Required').min(1).max(31),
  month: Yup.number().required('Required').min(1).max(12),
  year: Yup.number().min(1900).max(new Date().getFullYear()),
});

export const LoginSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().required('Required'),
});

export const SignupSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().required('Required'),
  re_password: Yup.string().oneOf(
    [Yup.ref('password'), null],
    'Passwords must match'
  ),
});

export const SetEmailSchema = Yup.object().shape({
  new_email: Yup.string().email('Invalid email').required('Required'),
  re_new_email: Yup.string()
    .email('Invalid email')
    .oneOf([Yup.ref('new_email'), null], 'Emails must match'),
  current_password: Yup.string().required('Required'),
});

export const SetPasswordSchema = Yup.object().shape({
  new_password: Yup.string().required('Required'),
  re_new_password: Yup.string().oneOf(
    [Yup.ref('new_password'), null],
    'New passwords must match'
  ),
  current_password: Yup.string().required('Required'),
});

export const SendResetPasswordEmailSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email').required('Required'),
});

export const ResetPasswordSchema = Yup.object().shape({
  new_password: Yup.string().required('Required'),
  re_new_password: Yup.string().oneOf(
    [Yup.ref('new_password'), null],
    'New passwords must match'
  ),
});
