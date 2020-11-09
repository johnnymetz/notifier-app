This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev

# cypress
npm run cypress:open
```

## Todo

- Add cypress tests for signup, set email and set password
  - Redirect to login when logged in and trying to visit signup, activate account, reset password, etc.
- Dry up formik code with generic form fields
- Check out [react-notification-system](https://github.com/igorprado/react-notification-system)

## Later

- Look into Next Redux (store exists on both client and server)

## Resources

- [Route protection](https://www.mikealche.com/software-development/how-to-implement-authentication-in-next-js-without-third-party-libraries)
- [Axios error handling](https://gist.github.com/fgilio/230ccd514e9381fafa51608fcf137253)
- [next-redux-wrapper](https://github.com/kirill-konshin/next-redux-wrapper)
- [More cool loading icons](https://youtu.be/AW0eFKDhAFg)
- [Another cool loading icon](https://youtu.be/xSNlsSfvwac)
- [Deploy next app to heroku](https://github.com/mars/heroku-nextjs)
