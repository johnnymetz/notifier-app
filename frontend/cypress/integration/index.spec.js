const serverUrl = Cypress.env('serverUrl');
const qaUserEmail = Cypress.env('qaUserEmail');
const qaUserPassword = Cypress.env('qaUserPassword');

context('Index', () => {
  beforeEach(() => {
    // TODO: fix deprecated commands
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
    cy.contains('h5', "Today's Events");
    cy.contains('h5', 'Upcoming Events');
    cy.contains('h5', 'Add an Event');
    cy.contains('h5', 'All Events');
  });

  it('display events today', () => {
    cy.seedQaUser('relative');
    cy.login(qaUserEmail, qaUserPassword);
    cy.visit('/');

    cy.get('[data-test=today-events-list]>.list-group-item').as('events');
    cy.get('@events')
      .should('have.length', 2)
      .and('contain', 'Event1')
      .and('contain', 'Event2');
  });

  it('display events upcoming', () => {
    cy.seedQaUser('relative');
    cy.login(qaUserEmail, qaUserPassword);
    cy.visit('/');

    cy.get('[data-test=upcoming-events-list]>.list-group-item').as('events');
    cy.get('@events')
      .should('have.length', 2)
      .and('contain', 'Event4')
      .and('contain', 'Event5');
  });

  it('display all events table', () => {
    cy.get('[data-test=all-events-list]>tbody>tr').as('rows');
    cy.get('@rows').should('have.length', 4);

    cy.get('@rows').contains('td', 'Event1');
    cy.get('@rows').contains('td', '01-24');
    cy.get('@rows').contains('td', 'Birthday');

    cy.get('@rows').contains('td', 'Event4');
    cy.get('@rows').contains('td', '12-31-1999');
    cy.get('@rows').contains('td', 'Holiday');
  });

  it('filter all events table', () => {
    cy.get('[data-test=all-events-list-search]').type('Event3');
    cy.get('[data-test=all-events-list]>tbody>tr')
      .its('length')
      .should('eq', 1);
    cy.get('[data-test=all-events-count').contains(1);
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
    cy.get('[data-test=all-events-list]>tbody>tr').as('rows');
    cy.get('@rows').should('have.length', 4);
    cy.get('[data-test=all-events-count').contains(4);

    cy.get('[data-test=create-event-name-input]').type('JJ Reddick');
    cy.get('[data-test=create-event-month-input]').select('06');
    cy.get('[data-test=create-event-day-input]').type('24');
    cy.get('[data-test=create-event-year-input]').type('1984');
    cy.get('[data-test=create-event-type-input]').select('Other');
    cy.get('[data-test=create-event-form]').submit();

    cy.wait('@addEvent').its('status').should('eq', 201);
    cy.wait('@getUser').its('status').should('eq', 200);
    // cy.get('@rows').should('have.length', 5); // bug: assertion hangs indefinitely
    cy.get('[data-test=all-events-list]>tbody>tr').should('have.length', 5);
    cy.get('[data-test=all-events-count').contains(5);
    cy.get('@rows').contains('td', 'JJ Reddick');
    cy.get('@rows').contains('td', '06-24');
    cy.get('@rows').contains('td', 'Other');
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
    cy.get('[data-test=all-events-list]>tbody>tr').as('rows');
    cy.get('@rows').should('have.length', 4);
    cy.get('@rows').first().as('firstRow');
    cy.get('@rows')
      .should('not.contain', 'JJ Reddick')
      .and('not.contain', '06-24')
      .and('not.contain', 'Other');

    cy.get('@firstRow').find('.ellipsis-dropdown-toggle').click();
    cy.get('@firstRow').contains('Edit').click();
    cy.get('[data-test=update-event-name-input]').clear().type('JJ Reddick');
    cy.get('[data-test=update-event-month-input]').select('06');
    cy.get('[data-test=update-event-day-input]').clear().type('24');
    cy.get('[data-test=update-event-type-input]').select('Other');
    cy.get('[data-test=update-event-form]').submit();

    cy.wait('@editEvent').its('status').should('eq', 200);
    cy.wait('@getUser').its('status').should('eq', 200);
    cy.get('@rows').should('have.length', 4);
    cy.get('[data-test=all-events-count').contains(4);
    cy.get('@rows')
      .should('contain', 'JJ Reddick')
      .and('contain', '06-24')
      .and('contain', 'Other');
  });

  it('delete event', () => {
    cy.get('[data-test=all-events-list]>tbody>tr').as('rows');
    cy.get('@rows').should('have.length', 4);
    cy.get('@rows').should('contain', 'Event1');
    cy.get('[data-test=all-events-count').contains(4);

    cy.get('@rows').first().as('firstRow');
    cy.get('@firstRow').find('.ellipsis-dropdown-toggle').click();
    cy.get('@firstRow').contains('Delete').click();
    cy.get('[data-test=confirm-modal-btn]').click();

    cy.wait('@deleteEvent').its('status').should('eq', 204);
    cy.wait('@getUser').its('status').should('eq', 200);
    cy.get('@rows').should('have.length', 3);
    cy.get('[data-test=all-events-count').contains(3);
    cy.get('@rows').should('not.contain', 'Event1');
  });
});
