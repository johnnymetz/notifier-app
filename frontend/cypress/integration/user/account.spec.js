const qaUserEmail = Cypress.env('qaUserEmail');
const qaUserEmail2 = Cypress.env('qaUserEmail2');
const qaUserPassword = Cypress.env('qaUserPassword');
const qaUserPassword2 = '123456';

context('Account', () => {
  beforeEach(() => {
    cy.seedQaUser();
    cy.login(qaUserEmail, qaUserPassword);
    cy.visit('/account');
  });

  it('navigate to account page via navbar', () => {
    cy.visit('/');
    cy.get('[data-test=navbar-account-link]').click();
    cy.location('pathname').should('eq', '/account');
  });

  it('display header', () => {
    cy.contains('h5', 'Account Settings');
  });

  /////////////////////////////
  // CHANGE EMAIL
  /////////////////////////////

  it('display feedback with no field values when changing email', () => {
    cy.get('[data-test=account-change-email]').click();
    cy.get('[data-test=set-email-new-email]').type('{enter}');
    cy.get('[data-test=set-email-new-email-invalid-feedback]').contains(
      'Required'
    );
    cy.get('[data-test=set-email-re-new-email-invalid-feedback]').contains(
      'Required'
    );
    cy.get('[data-test=set-email-current-password-invalid-feedback]').contains(
      'Required'
    );
  });

  it('display feedback with mismatching emails when changing email', () => {
    cy.get('[data-test=account-change-email]').click();
    cy.get('[data-test=set-email-new-email]').type(qaUserEmail);
    cy.get('[data-test=set-email-re-new-email]').type(`${qaUserEmail2}{enter}`);
    cy.get('[data-test=set-email-re-new-email-invalid-feedback]').contains(
      'Emails must match'
    );
  });

  it('display feedback with duplicate email when changing email', () => {
    cy.get('[data-test=account-change-email]').click();
    cy.get('[data-test=set-email-new-email]').type(qaUserEmail);
    cy.get('[data-test=set-email-re-new-email]').type(qaUserEmail);
    cy.get('[data-test=set-email-current-password]').type(
      `${qaUserPassword}{enter}`
    );
    cy.get('[data-test=set-email-new-email-invalid-feedback]').contains(
      'user with this email address already exists.'
    );
  });

  it('display feedback with incorrect password when changing email', () => {
    cy.get('[data-test=account-change-email]').click();
    cy.get('[data-test=set-email-new-email]').type(qaUserEmail2);
    cy.get('[data-test=set-email-re-new-email]').type(qaUserEmail2);
    cy.get('[data-test=set-email-current-password]').type('bad{enter}');
    cy.get('[data-test=set-email-current-password-invalid-feedback]').contains(
      'Invalid password.'
    );
  });

  it('successfully change email', () => {
    cy.get('[data-test=account-email]').contains(qaUserEmail);
    cy.get('[data-test=account-change-email]').click();
    cy.get('[data-test=set-email-new-email]').type(qaUserEmail2);
    cy.get('[data-test=set-email-re-new-email]').type(qaUserEmail2);
    cy.get('[data-test=set-email-current-password]').type(
      `${qaUserPassword}{enter}`
    );
    cy.get('[role=alert]').should('include.text', 'Email successfully changed');
    cy.get('[data-test=account-email]').contains(qaUserEmail2);
  });

  /////////////////////////////
  // CHANGE PASSWORD
  /////////////////////////////

  it('display feedback with no field values when changing password', () => {
    cy.get('[data-test=account-change-password]').click();
    cy.get('[data-test=set-password-new-password]').type('{enter}');
    cy.get('[data-test=set-password-new-password-invalid-feedback]').contains(
      'Required'
    );
    cy.get(
      '[data-test=set-password-re-new-password-invalid-feedback]'
    ).contains('Required');
    cy.get(
      '[data-test=set-password-current-password-invalid-feedback]'
    ).contains('Required');
  });

  it('display feedback with mismatching passwords when changing password', () => {
    cy.get('[data-test=account-change-password]').click();
    cy.get('[data-test=set-password-new-password]').type(qaUserPassword);
    cy.get('[data-test=set-password-re-new-password]').type(
      `${qaUserPassword2}{enter}`
    );
    cy.get(
      '[data-test=set-password-re-new-password-invalid-feedback]'
    ).contains('New passwords must match');
  });

  it('display feedback with incorrect current password when changing password', () => {
    cy.get('[data-test=account-change-password]').click();
    cy.get('[data-test=set-password-new-password]').type(qaUserPassword2);
    cy.get('[data-test=set-password-re-new-password]').type(qaUserPassword2);
    cy.get('[data-test=set-password-current-password]').type('bad{enter}');
    cy.get(
      '[data-test=set-password-current-password-invalid-feedback]'
    ).contains('Invalid password.');
  });

  it('successfully change password', () => {
    cy.get('[data-test=account-change-password]').click();
    cy.get('[data-test=set-password-new-password]').type(qaUserPassword2);
    cy.get('[data-test=set-password-re-new-password]').type(qaUserPassword2);
    cy.get('[data-test=set-password-current-password]').type(
      `${qaUserPassword}{enter}`
    );
    cy.get('[role=alert]').should(
      'include.text',
      'Password successfully changed'
    );
    cy.login(qaUserEmail, qaUserPassword2);
  });

  /////////////////////////////
  // CHANGE SUBSCRIPTION FLAG
  /////////////////////////////

  it('successfully change subscription flag', () => {
    // two ways of validating checkbox state
    cy.get('#send-me-a-daily-morning-email').should('have.attr', 'checked');
    cy.get('#send-me-a-daily-morning-email').should('be.checked');
    cy.get('#send-me-a-daily-morning-email').uncheck();
    cy.get('#send-me-a-daily-morning-email').should('not.have.attr', 'checked');
    cy.get('#send-me-a-daily-morning-email').should('not.be.checked');
  });
});
