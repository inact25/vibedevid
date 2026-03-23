const fs = require('fs');
const file = 'tests/project-submit.spec.ts';
let content = fs.readFileSync(file, 'utf8');

content = content.replace(
  "await expect(page.getByText('Required. Explain your project (min 30 chars, max 1500 chars).')).toBeVisible()",
  "await expect(page.getByText('Required. Explain your project (min 30 chars, max 1600 chars).')).toBeVisible()"
);
fs.writeFileSync(file, content, 'utf8');
