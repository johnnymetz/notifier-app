import * as Yup from 'yup';

export const LoginSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().required('Required'),
});

export const SignupSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().required('Required'),
  re_password: Yup.string().required('Required'),
});

export const FriendSchema = Yup.object().shape({
  name: Yup.string().required('Required'),
  day: Yup.number().required('Required').min(1).max(31),
  month: Yup.number().required('Required').min(1).max(12),
  year: Yup.number().min(1900).max(new Date().getFullYear()),
});
