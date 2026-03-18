#!/usr/bin/env node
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');

const html = readFileSync('public/index.html', 'utf8');
const experienceHtml = extractExperienceSection(html);

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function attributeEqualsPattern(attributeName, attributeValue) {
  const escapedName = escapeRegex(attributeName);
  const escapedValue = escapeRegex(String(attributeValue));
  return `\\b${escapedName}\\s*=\\s*(?:"${escapedValue}"|'${escapedValue}'|${escapedValue})(?=[\\s/>])`;
}

function tagRegex(attributeMap, flags) {
  const pattern = Object.entries(attributeMap)
    .map(
      ([attributeName, attributeValue]) =>
        `(?=[^>]*${attributeEqualsPattern(attributeName, attributeValue)})`
    )
    .join('');
  return new RegExp(`<[^>]+${pattern}[^>]*>`, flags);
}

function indexOfSectionOpeningTag(sourceHtml, sectionId) {
  const sectionIdPattern = attributeEqualsPattern('id', sectionId);
  const sectionPattern = new RegExp(`<section\\b(?=[^>]*${sectionIdPattern})[^>]*>`, 'i');
  const match = sectionPattern.exec(sourceHtml);
  return match ? match.index : -1;
}

function extractExperienceSection(sourceHtml) {
  const experienceStart = indexOfSectionOpeningTag(sourceHtml, 'experience');
  assert.notStrictEqual(experienceStart, -1, 'Missing fragment: Experience section');

  const htmlAfterExperience = sourceHtml.slice(experienceStart);
  const projectsBoundary = indexOfSectionOpeningTag(htmlAfterExperience, 'projects');
  assert.notStrictEqual(projectsBoundary, -1, 'Missing fragment: Projects section boundary');

  return htmlAfterExperience.slice(0, projectsBoundary);
}

function indexOfTag(attrs) {
  const match = tagRegex(attrs, 'i').exec(experienceHtml);
  return match ? match.index : -1;
}

function indexOfOrThrow(attrs, label) {
  const index = indexOfTag(attrs);
  assert.notStrictEqual(index, -1, `Missing fragment: ${label}`);
  return index;
}

function countTags(attrs) {
  const matches = experienceHtml.match(tagRegex(attrs, 'gi'));
  return matches ? matches.length : 0;
}

const quokkaAnchor = indexOfOrThrow(
  { 'data-consulting-group': 'software by quokka', 'data-timeline-kind': 'anchor' },
  'Software by Quokka anchor'
);
const zeekrChild = indexOfOrThrow(
  {
    'data-consulting-group': 'software by quokka',
    'data-timeline-kind': 'child',
    'data-company': 'Zeekr Technology Europe',
  },
  'Zeekr child'
);
assert.ok(quokkaAnchor < zeekrChild, 'Expected Software by Quokka anchor before Zeekr child');

const globantAnchor = indexOfOrThrow(
  { 'data-consulting-group': 'globant', 'data-timeline-kind': 'anchor' },
  'Globant anchor'
);
const jcpenneyChild = indexOfOrThrow(
  {
    'data-consulting-group': 'globant',
    'data-timeline-kind': 'child',
    'data-company': 'JCPenney',
  },
  'JCPenney child'
);
const adobeChild = indexOfOrThrow(
  {
    'data-consulting-group': 'globant',
    'data-timeline-kind': 'child',
    'data-company': 'Adobe',
  },
  'Adobe child'
);
indexOfOrThrow(
  { 'data-consulting-group': 'dadosfera', 'data-timeline-kind': 'anchor' },
  'Dadosfera anchor'
);

assert.ok(globantAnchor < jcpenneyChild, 'Expected Globant anchor before JCPenney child');
assert.ok(jcpenneyChild < adobeChild, 'Expected Globant children to preserve source order');

assert.equal(
  countTags({ 'data-consulting-group': 'software by quokka', 'data-timeline-kind': 'anchor' }),
  1
);
assert.equal(countTags({ 'data-consulting-group': 'globant', 'data-timeline-kind': 'anchor' }), 1);
assert.equal(
  countTags({ 'data-consulting-group': 'dadosfera', 'data-timeline-kind': 'anchor' }),
  1
);

assert.equal(
  countTags({ 'data-company': 'Zeekr Technology Europe' }),
  1,
  'Expected Zeekr to render once'
);
