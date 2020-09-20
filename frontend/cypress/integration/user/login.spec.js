const qaUserEmail = Cypress.env('qaUserEmail');
const qaUserPassword = Cypress.env('qaUserPassword');

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
    cy.contains('h2', 'Login');
  });

  it('display feedback with no credentials', () => {
    cy.get('form').contains('Submit').click();
    cy.get('[data-test=email-invalid-feedback]').contains('Required');
    cy.get('[data-test=password-invalid-feedback]').contains('Required');
  });

  it('display feedback with invalid email', () => {
    cy.get('[data-test=email]').type('bad{enter}');
    cy.get('[data-test=email-invalid-feedback]').contains('Invalid email');
  });

  it('raise alert with bad credentials', () => {
    cy.get('[data-test=email]').type('bad@email.com');
    cy.get('[data-test=password]').type('bad{enter}');
    cy.get('[role=alert]').should('include.text', 'No active account found');
  });

  it('navigate to home page with valid credentials', () => {
    cy.get('[data-test=email]').type(qaUserEmail);
    cy.get('[data-test=password]').type(`${qaUserPassword}{enter}`);
    cy.location('pathname').should('eq', '/');
  });
});
