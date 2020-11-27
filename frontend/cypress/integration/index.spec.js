const serverUrl = Cypress.env('serverUrl');
const qaUserEmail = Cypress.env('qaUserEmail');
const qaUserPassword = Cypress.env('qaUserPassword');

context('Index', () => {
  beforeEach(() => {
    cy.server();
    cy.route('GET', '/api/auth/users/me/').as('getUser');
    cy.route('POST', '/api/friends/').as('addFriend');
    cy.route('PATCH', '/api/friends/*').as('editFriend');
    cy.route('DELETE', '/api/friends/*').as('deleteFriend');

    cy.seedQaUser();
    cy.login(qaUserEmail, qaUserPassword);
    cy.visit('/');
  });

  it('log out', () => {
    cy.get('a').contains('Logout').click();
    cy.location('pathname').should('eq', '/login');
  });

  it('display headers', () => {
    cy.contains('h5', 'Upcoming');
    cy.contains('h5', 'Add Friend');
    cy.contains('h5', 'All Friends');
  });

  it('display friends table', () => {
    cy.get('[data-test=friends-list]>tbody>tr').as('rows');
    cy.get('@rows').should('have.length', 4);
    cy.get('@rows').contains('td', 'Friend1');
    cy.get('@rows').contains('td', '03-28');
  });

  it('filter friends table', () => {
    cy.get('[data-test=friends-list-search]').type('Friend1');
    cy.get('[data-test=friends-list]>tbody>tr').its('length').should('eq', 1);
  });

  it('clicking month label toggles dropdown values', () => {
    cy.get('[data-test=create-friend-month-input]')
      .find(':selected')
      .contains('01');
    cy.contains('label', 'Month').click();
    cy.get('[data-test=create-friend-month-input]')
      .find(':selected')
      .contains('January');
    cy.contains('label', 'Month').click();
    cy.get('[data-test=create-friend-month-input]')
      .find(':selected')
      .contains('01');
  });

  it('add friend', () => {
    cy.get('[data-test=friends-list]>tbody>tr').as('rows');
    cy.get('@rows').should('have.length', 4);

    cy.get('[data-test=create-friend-name-input]').type('JJ Reddick');
    cy.get('[data-test=create-friend-month-input]').select('06');
    cy.get('[data-test=create-friend-day-input]').type('24');
    cy.get('[data-test=create-friend-year-input]').type('1984{enter}');

    cy.wait('@addFriend').its('status').should('eq', 201);
    cy.wait('@getUser').its('status').should('eq', 200);
    // cy.get('@rows').should('have.length', 5); // bug: assertion hangs indefinitely
    cy.get('[data-test=friends-list]>tbody>tr').should('have.length', 5);
    cy.get('@rows').contains('td', 'JJ Reddick');
  });

  it('display feedback with no values on add friend', () => {
    cy.get('[data-test=create-friend-name-input]').type('{enter}');
    cy.get('[data-test=create-friend-name-input]')
      .siblings('.invalid-feedback')
      .contains('Required');
    cy.get('[data-test=create-friend-day-input]')
      .siblings('.invalid-feedback')
      .contains('Required');
  });

  it('update friend', () => {
    cy.get('[data-test=friends-list]>tbody>tr').as('rows');
    cy.get('@rows').should('have.length', 4);
    cy.get('@rows').first().as('firstRow');
    cy.get('@firstRow').should('contain', 'Friend1').and('contain', '03-28');

    cy.get('@firstRow').find('.ellipsis-dropdown-toggle').click();
    cy.get('@firstRow').contains('Edit').click();
    cy.get('[data-test=update-friend-name-input]').clear().type('JJ Reddick');
    cy.get('[data-test=update-friend-month-input]').select('06');
    cy.get('[data-test=update-friend-day-input]').clear().type('24{enter}');

    cy.wait('@editFriend').its('status').should('eq', 200);
    cy.wait('@getUser').its('status').should('eq', 200);
    cy.get('@rows').should('have.length', 4);
    cy.get('@firstRow').should('contain', 'JJ Reddick').and('contain', '06-24');
  });

  it('delete friend', () => {
    cy.get('[data-test=friends-list]>tbody>tr').as('rows');
    cy.get('@rows').should('have.length', 4);
    cy.get('@rows').should('contain', 'Friend1').and('contain', '03-28');

    cy.get('@rows').first().as('firstRow');
    cy.get('@firstRow').find('.ellipsis-dropdown-toggle').click();
    cy.get('@firstRow').contains('Delete').click();
    cy.get('[data-test=confirm-modal-btn]').click();

    cy.wait('@deleteFriend').its('status').should('eq', 204);
    cy.wait('@getUser').its('status').should('eq', 200);
    cy.get('@rows').should('have.length', 3);
    cy.get('@rows')
      .should('not.contain', 'Friend1')
      .and('not.contain', '03-28');
  });
});