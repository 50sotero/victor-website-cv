#!/usr/bin/env node
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');

const homepageHtml = readFileSync('public/index.html', 'utf8');
const cvHtml = readFileSync('public/cv/index.html', 'utf8');

const expectedIcons = ['anthropic', 'databricks', 'university', 'cambridge'];

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function attributeEqualsPattern(attributeName, attributeValue) {
  const escapedName = escapeRegex(attributeName);
  const escapedValue = escapeRegex(String(attributeValue));
  return `\\b${escapedName}\\s*=\\s*(?:"${escapedValue}"|'${escapedValue}'|${escapedValue})(?=[\\s/>])`;
}

function classContainsPattern(className) {
  const escapedClassName = escapeRegex(className);
  return `\\bclass\\s*=\\s*(?:"[^"]*${escapedClassName}[^"]*"|'[^']*${escapedClassName}[^']*'|[^\\s>]*${escapedClassName}[^\\s>]*)`;
}

function assertLogo(html, iconName, context) {
  const iconPattern = new RegExp(
    `<[^>]+(?=[^>]*${classContainsPattern(context)})(?=[^>]*${attributeEqualsPattern('data-certification-icon', iconName)})[^>]*>`,
    'i'
  );
  assert.ok(iconPattern.test(html), `Expected ${context} ${iconName} certification logo`);
}

for (const iconName of expectedIcons) {
  assertLogo(homepageHtml, iconName, 'certification-logo');
  assertLogo(cvHtml, iconName, 'cv-certification-logo');
}
