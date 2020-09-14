// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

const serverUrl = Cypress.env('serverUrl');
const qaUserEmail = Cypress.env('qaUserEmail');

// -- This is a parent command --
Cypress.Commands.add('login', (email, password) => {
  cy.request('POST', `${serverUrl}/auth/jwt/create/`, {
    email,
    password,
  }).then(res => {
    localStorage.setItem('accessToken', res.body.access);
    localStorage.setItem('refreshToken', res.body.refresh);
  });
});

Cypress.Commands.add('seedQaUser', () => {
  cy.request('POST', `${serverUrl}/seed/qa-user/`, {
    auth: 'Cypress789',
  }).should(res => {
    expect(res.status).to.eq(201);
    expect(res.body.email).to.eq(qaUserEmail);
  });
});

// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })
