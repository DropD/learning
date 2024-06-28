const { UserInputError } = require('apollo-server-express');
const { getDb, getNextSequence } = require('./db.js');

async function get(_, { id }) {
  const db = getDb();
  const issue = await db.collection('issues').findOne({ id });
  return issue;
}

async function list(_, { status, effortMin, effortMax }) {
  const db = getDb();
  const filter = {};
  if (status) filter.status = status;
  if (effortMin !== undefined || effortMax !== undefined) {
    filter.effort = {};
    if (effortMin !== undefined) filter.effort.$gte = effortMin;
    if (effortMax !== undefined) filter.effort.$lte = effortMax;
  }
  const issues = await db.collection('issues').find(filter).toArray();
  return issues;
}

function validateIssue(issue) {
  const errors = [];
  if (issue.title.length < 3) {
    errors.push('Field "title" must be at least 3 characters long.');
  }
  if (issue.status === 'Assigned' && !issue.owner) {
    errors.push('Field "owner" is required when status is "Assigned"');
  }
  if (errors.length > 0) {
    throw new UserInputError('Invalid input(s)', { errors });
  }
}

async function add(_, { issue }) {
  const db = getDb();
  const issues = await db.collection('issues');
  validateIssue(issue);
  const newIssue = Object.assign({}, issue);
  newIssue.created = new Date();
  newIssue.id = await getNextSequence('issues');
  const result = await issues.insertOne(newIssue);
  const savedIssue = await issues.findOne({ _id: result.insertedId });
  return savedIssue;
}

async function update(_, { id, changes }) {
  const db = getDb();
  const issues = await db.collection('issues');
  if (changes.title || changes.status || changes.owner) {
    const issue = await issues.findOne({ id });
    Object.assign(issue, changes);
    validateIssue(issue);
  }
  await issues.updateOne({ id }, { $set: changes });
  const savedIssue = await issues.findOne({ id });
  return savedIssue;
}

async function remove(_, { id }) {
  const db = getDb();
  const issues = await db.collection('issues');
  const trash = await db.collection('deleted_issues');
  const issue = await issues.findOne({ id });
  if (!issue) return false;
  issue.deleted = new Date();
  let result = await trash.insertOne(issue);
  if (result.insertedId) {
    result = await issues.deleteOne({ id });
    return result.deletedCount === 1;
  }
  return false
}

module.exports = { list, add, get, update, remove };
