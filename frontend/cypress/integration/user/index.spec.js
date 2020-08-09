const serverUrl = Cypress.env('serverUrl');

context('Index', () => {
  beforeEach(() => {
    cy.login('qa', 'pw');
    cy.visit('/');
  });

  it('logs out', () => {
    cy.get('a').contains('Logout').click();
    cy.location('pathname').should('eq', '/login');
  });

  it('displays headers', () => {
    cy.contains('h2', 'Welcome');
    cy.contains('h4', 'Upcoming');
    cy.contains('h4', 'Add Friend');
    cy.contains('h4', 'Friends');
  });

  it('displays friends table', () => {
    cy.get('tbody>tr').its('length').should('eq', 4);
    cy.get('tbody>tr').eq(0).as('firstRow');
    cy.get('@firstRow').find('td').should('include.text', 'Friend1');
    cy.get('@firstRow').find('td').should('include.text', '03-28');
  });

  it('filter friends table', () => {
    cy.get('[data-test=search]').type('Friend1');
    cy.get('tbody>tr').its('length').should('eq', 1);
  });

  // it('add a friend', () => {});
  // it('requires name, month and day to add a friend', () => {});

  // it('update a friend', () => {});
  // it('requires name, month and day to update a friend', () => {});

  // it('delete a friend', () => {});
});
