context('Login', () => {
  beforeEach(() => {
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
      'Username and password fields required'
    );
  });

  it('raise alert with bad credentials', () => {
    cy.get('[data-test=username]').type('bad');
    cy.get('[data-test=password]').type('bad{enter}');
    cy.get('[role=alert]').should('include.text', 'No active account found');
  });

  it('navigate to home page with valid credentials', () => {
    cy.get('[data-test=username]').type('qa');
    cy.get('[data-test=password]').type('qa{enter}');
    cy.location('pathname').should('eq', '/');
  });
});
