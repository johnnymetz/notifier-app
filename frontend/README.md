# Frontend

This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Todo

- Add cypress tests to...
  - Unit test helper functions
  - Ensure pressing eye icon displays password
  - Ensure redirect to login when logged in and trying to visit:
    - signup, activate account, reset password, etc.

## Later

- Check out Next-auth
- Check out react-query or swr library for data fetching
- Add a chart

## Resources

- [Route protection][url1]
- [Axios error handling](https://gist.github.com/fgilio/230ccd514e9381fafa51608fcf137253)
- [next-redux-wrapper](https://github.com/kirill-konshin/next-redux-wrapper)
- [More cool loading icons](https://youtu.be/AW0eFKDhAFg)
- [Another cool loading icon](https://youtu.be/xSNlsSfvwac)
- [Deploy next app to heroku](https://github.com/mars/heroku-nextjs)
- [react-notification-system](https://github.com/igorprado/react-notification-system)

## Update packages

```
npm install -g npm-check-updates
ncu  # show any updates
ncu -u cypress  # update cypress in package.json
npm install
npm list --depth 0
```

[url1]: https://www.mikealche.com/software-development/how-to-implement-authentication-in-next-js-without-third-party-libraries
