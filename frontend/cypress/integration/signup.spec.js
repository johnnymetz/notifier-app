const qaUserEmail = Cypress.env('QA_USER_EMAIL1');
const qaUserPassword = Cypress.env('QA_USER_PASSWORD');

context('Signup', () => {
  beforeEach(() => {
    cy.deleteQaUser();
    cy.visit('/signup');
  });

  it('navigate to signup page from login page', () => {
    cy.visit('/login');
    cy.get('[data-test=login-to-signup-link]').click();
    cy.location('pathname').should('eq', '/signup');
  });

  it('display header', () => {
    cy.contains('h4', 'Sign Up');
  });

  it('display feedback with no field values', () => {
    cy.get('form').contains('Sign Up').click();
    cy.get('[data-test=signup-email-invalid-feedback]').contains('Required');
    cy.get('[data-test=signup-password-invalid-feedback]').contains('Required');
    cy.get('[data-test=signup-re-password-invalid-feedback]').contains(
      'Required'
    );
  });

  it('display feedback with invalid email', () => {
    cy.get('[data-test=signup-email]').type('bad{enter}');
    cy.get('[data-test=signup-email-invalid-feedback]').contains(
      'Invalid email'
    );
  });

  it('display feedback with mismatching passwords', () => {
    cy.get('[data-test=signup-password]').type(`123{enter}`);
    cy.get('[data-test=signup-re-password]').type(`456{enter}`);
    cy.get('[data-test=signup-re-password-invalid-feedback]').contains(
      'Passwords must match'
    );
  });

  it('display feedback with duplicate email', () => {
    cy.seedQaUser();
    cy.get('[data-test=signup-email]').type(`${qaUserEmail}{enter}`);
    cy.get('[data-test=signup-password]').type(`${qaUserPassword}{enter}`);
    cy.get('[data-test=signup-re-password]').type(`${qaUserPassword}{enter}`);
    cy.get('[data-test=signup-email-invalid-feedback]').contains(
      'user with this email address already exists.'
    );
  });

  it('navigate to login page with valid submission but cant login', () => {
    cy.get('[data-test=signup-email]').type(`${qaUserEmail}{enter}`);
    cy.get('[data-test=signup-password]').type(`${qaUserPassword}{enter}`);
    cy.get('[data-test=signup-re-password]').type(`${qaUserPassword}{enter}`);
    cy.get('[role=alert]').should(
      'include.text',
      'Your account was successfully created! Check your email to activate it.'
    );
    cy.location('pathname').should('eq', '/login');
    cy.get('[data-test=login-email]').type(qaUserEmail);
    cy.get('[data-test=login-password]').type(`${qaUserPassword}{enter}`);
    cy.get('[role=alert]').should('include.text', 'No active account found');
  });
});
