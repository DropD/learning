const aboutMessage = 'Issue Tracker API v1.0';

function setMessage(_, { message }) {
  return message;
}

function getMessage() {
  return aboutMessage;
}

module.exports = { getMessage, setMessage };
