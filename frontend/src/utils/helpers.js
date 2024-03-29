import { toast } from 'react-toastify';

// TODO: add unit test (cypress should work)
export const handleDrfError = (error, fields, setFieldError) => {
  console.warn(error);
  if (typeof error === 'string') {
    toast.error(error);
  } else if (Array.isArray(error)) {
    toast.error(error[0]);
  } else {
    fields = fields || [];
    for (const field of fields) {
      if (error[field]) {
        setFieldError(field, error[field][0]);
      }
    }
    if (error.uid || error.token) {
      toast.error('Unable to authenticate user');
    }
    if (error.non_field_errors) {
      toast.error(error.non_field_errors[0]);
    }
    for (const [key, value] of Object.entries(error)) {
      if (!fields.includes(key)) {
        toast.error(value[0]);
      }
    }
  }
};

// needs to be awaited
export const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

// export const isObjectEmpty = obj =>
//   Object.entries(obj).length === 0 && obj.constructor === Object;

export const range = (start, end) => {
  const ans = [];
  for (let i = start; i < end; i++) {
    ans.push(i);
  }
  return ans;
};

// export const truncate = (str, length, suffix = '...') => {
//   if (str.length <= length) {
//     return str;
//   }
//   return str.slice(0, length - suffix.length) + suffix;
// };
