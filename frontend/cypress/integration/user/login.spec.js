context('Login', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('redirects to login if not authenticated on home page', () => {
    cy.visit('/');
    cy.location('pathname').should('eq', '/login');
  });

  it('displays header', () => {
    cy.contains('h2', 'Login');
  });

  it('requires username and password fields', () => {
    cy.get('form').contains('Submit').click();
    cy.get('[role=alert]').should(
      'have.text',
      'Username and password fields required'
    );
  });

  it('displays error message with bad credentials', () => {
    cy.get('[data-test=username]').type('bad');
    cy.get('[data-test=password]').type('bad{enter}');
    cy.get('[role=alert]').should('include.text', 'No active account found');
  });

  it('navigates to home page with valid credentials', () => {
    cy.get('[data-test=username]').type('qa');
    cy.get('[data-test=password]').type('pw{enter}');
    cy.location('pathname').should('eq', '/');
  });
});
