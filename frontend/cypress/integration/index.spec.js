const serverUrl = Cypress.env('serverUrl');
const qaUserEmail = Cypress.env('qaUserEmail');
const qaUserPassword = Cypress.env('qaUserPassword');

context('Index', () => {
  beforeEach(() => {
    cy.server();
    cy.route('GET', '/api/auth/users/me/').as('getUser');
    cy.route('POST', '/api/events/').as('addEvent');
    cy.route('PATCH', '/api/events/*').as('editEvent');
    cy.route('DELETE', '/api/events/*').as('deleteEvent');

    cy.seedQaUser();
    cy.login(qaUserEmail, qaUserPassword);
    cy.visit('/');
  });

  it('log out', () => {
    cy.get('a').contains('Logout').click();
    cy.location('pathname').should('eq', '/login');
  });

  it('display headers', () => {
    cy.contains('h5', 'Upcoming Events');
    cy.contains('h5', 'Add an Event');
    cy.contains('h5', 'All Events');
  });

  it('display events table', () => {
    cy.get('[data-test=events-list]>tbody>tr').as('rows');
    cy.get('@rows').should('have.length', 4);
    cy.get('@rows').contains('td', 'Event1');
    cy.get('@rows').contains('td', '03-28');
  });

  it('filter events table', () => {
    cy.get('[data-test=events-list-search]').type('Event1');
    cy.get('[data-test=events-list]>tbody>tr').its('length').should('eq', 1);
  });

  it('clicking month label toggles dropdown values', () => {
    cy.get('[data-test=create-event-month-input]')
      .find(':selected')
      .contains('01');
    cy.contains('label', 'Month').click();
    cy.get('[data-test=create-event-month-input]')
      .find(':selected')
      .contains('January');
    cy.contains('label', 'Month').click();
    cy.get('[data-test=create-event-month-input]')
      .find(':selected')
      .contains('01');
  });

  it('add event', () => {
    cy.get('[data-test=events-list]>tbody>tr').as('rows');
    cy.get('@rows').should('have.length', 4);

    cy.get('[data-test=create-event-name-input]').type('JJ Reddick');
    cy.get('[data-test=create-event-month-input]').select('06');
    cy.get('[data-test=create-event-day-input]').type('24');
    cy.get('[data-test=create-event-year-input]').type('1984{enter}');

    cy.wait('@addEvent').its('status').should('eq', 201);
    cy.wait('@getUser').its('status').should('eq', 200);
    // cy.get('@rows').should('have.length', 5); // bug: assertion hangs indefinitely
    cy.get('[data-test=events-list]>tbody>tr').should('have.length', 5);
    cy.get('@rows').contains('td', 'JJ Reddick');
  });

  it('display feedback with no values on add event', () => {
    cy.get('[data-test=create-event-name-input]').type('{enter}');
    cy.get('[data-test=create-event-name-input]')
      .siblings('.invalid-feedback')
      .contains('Required');
    cy.get('[data-test=create-event-day-input]')
      .siblings('.invalid-feedback')
      .contains('Required');
  });

  it('update event', () => {
    cy.get('[data-test=events-list]>tbody>tr').as('rows');
    cy.get('@rows').should('have.length', 4);
    cy.get('@rows').first().as('firstRow');
    cy.get('@firstRow').should('contain', 'Event1').and('contain', '03-28');

    cy.get('@firstRow').find('.ellipsis-dropdown-toggle').click();
    cy.get('@firstRow').contains('Edit').click();
    cy.get('[data-test=update-event-name-input]').clear().type('JJ Reddick');
    cy.get('[data-test=update-event-month-input]').select('06');
    cy.get('[data-test=update-event-day-input]').clear().type('24{enter}');

    cy.wait('@editEvent').its('status').should('eq', 200);
    cy.wait('@getUser').its('status').should('eq', 200);
    cy.get('@rows').should('have.length', 4);
    cy.get('@firstRow').should('contain', 'JJ Reddick').and('contain', '06-24');
  });

  it('delete event', () => {
    cy.get('[data-test=events-list]>tbody>tr').as('rows');
    cy.get('@rows').should('have.length', 4);
    cy.get('@rows').should('contain', 'Event1').and('contain', '03-28');

    cy.get('@rows').first().as('firstRow');
    cy.get('@firstRow').find('.ellipsis-dropdown-toggle').click();
    cy.get('@firstRow').contains('Delete').click();
    cy.get('[data-test=confirm-modal-btn]').click();

    cy.wait('@deleteEvent').its('status').should('eq', 204);
    cy.wait('@getUser').its('status').should('eq', 200);
    cy.get('@rows').should('have.length', 3);
    cy.get('@rows').should('not.contain', 'Event1').and('not.contain', '03-28');
  });
});
