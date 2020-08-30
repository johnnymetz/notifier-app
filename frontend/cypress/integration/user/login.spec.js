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

  it('raise alert with no credentials', () => {
    cy.get('form').contains('Submit').click();
    cy.get('[role=alert]').should(
      'have.text',
      'Email and password fields required'
    );
  });

  it('raise alert with bad credentials', () => {
    cy.get('[data-test=email]').type('bad');
    cy.get('[data-test=password]').type('bad{enter}');
    cy.get('[role=alert]').should('include.text', 'No active account found');
  });

  it('navigate to home page with valid credentials', () => {
    cy.get('[data-test=email]').type(qaUserEmail);
    cy.get('[data-test=password]').type(`${qaUserPassword}{enter}`);
    cy.location('pathname').should('eq', '/');
  });
});
