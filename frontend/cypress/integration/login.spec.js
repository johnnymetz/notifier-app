const qaUserEmail = Cypress.env('QA_USER_EMAIL1');
const qaUserPassword = Cypress.env('QA_USER_PASSWORD');

context('Login', () => {
  beforeEach(() => {
    cy.seedQaUser();
    cy.visit('/login');
  });

  it('redirect to login if not authenticated on home page', () => {
    cy.visit('/');
    cy.location('pathname').should('eq', '/login');
  });

  it('display header', () => {
    cy.contains('h4', 'Login');
  });

  it('display feedback with no credentials', () => {
    cy.get('form').contains('Continue').click();
    cy.get('[data-test=login-email-invalid-feedback]').contains('Required');
    cy.get('[data-test=login-password-invalid-feedback]').contains('Required');
  });

  it('display feedback with invalid email', () => {
    cy.get('[data-test=login-email]').type('bad{enter}');
    cy.get('[data-test=login-email-invalid-feedback]').contains(
      'Invalid email'
    );
  });

  it('raise alert with bad credentials', () => {
    cy.get('[data-test=login-email]').type('bad@email.com');
    cy.get('[data-test=login-password]').type('bad{enter}');
    cy.get('[role=alert]').should(
      'include.text',
      'No active account found with the given credentials'
    );
  });

  it('navigate to home page with valid credentials', () => {
    cy.get('[data-test=login-email]').type(qaUserEmail);
    cy.get('[data-test=login-password]').type(`${qaUserPassword}{enter}`);
    cy.location('pathname').should('eq', '/');
  });
});
