const serverUrl = Cypress.env('SERVER_URL');
const qaUserEmail = Cypress.env('QA_USER_EMAIL1');

Cypress.Commands.add('login', (email, password) => {
  const log = Cypress.log({
    message: [`🔐 Authenticating | ${email}`],
    autoEnd: false,
  });

  cy.request({
    method: 'POST',
    url: `${serverUrl}/auth/jwt/create/`,
    body: { email, password },
    log: false,
  }).then(res => {
    expect(res.status).to.eq(200);
    expect(res.body).to.have.keys('access', 'refresh');
    localStorage.setItem('accessToken', res.body.access);
    localStorage.setItem('refreshToken', res.body.refresh);
  });

  log.end();
});

Cypress.Commands.add('seedQaUser', dataset => {
  const log = Cypress.log({
    message: ['🌱 Seeding QA user in database'],
    autoEnd: false,
  });

  cy.request({
    method: 'POST',
    url: `${serverUrl}/seed/qa-user/`,
    body: { auth: 'Cypress789', dataset: dataset },
    log: false,
  }).should(res => {
    // Supress logs to reduce noise: https://github.com/cypress-io/cypress/issues/7693
    expect(res.status).to.eq(201);
    expect(res.body.email).to.eq(qaUserEmail);
  });

  log.end();
});

Cypress.Commands.add('deleteQaUser', () => {
  cy.request('DELETE', `${serverUrl}/seed/qa-user/`, {
    auth: 'Cypress789',
  }).should(res => {
    expect(res.status).to.eq(204);
  });
});
