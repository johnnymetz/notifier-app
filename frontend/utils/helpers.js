// TODO: add unit test (cypress should work)
export const handleDrfErrors = (error, fields, setFieldError) => {
  console.warn(error);
  if (typeof error === 'string') {
    toast.error(error);
  } else {
    for (const field of fields) {
      if (error[field]) {
        setFieldError(field, error[field][0]);
      }
    }
    if (error.non_field_errors) {
      toast.error(error.non_field_errors[0]);
    }
  }
};

// // needs to be awaited
// export const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

// export const isObjectEmpty = obj =>
//   Object.entries(obj).length === 0 && obj.constructor === Object;

// export const range = (start, end) => {
//   const ans = [];
//   for (let i = start; i < end; i++) {
//     ans.push(i);
//   }
//   return ans;
// };

// export const truncate = (str, length, suffix = '...') => {
//   if (str.length <= length) {
//     return str;
//   }
//   return str.slice(0, length - suffix.length) + suffix;
// };
