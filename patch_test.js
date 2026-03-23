const fs = require('fs');
const file = 'tests/project-submit.spec.ts';
let content = fs.readFileSync(file, 'utf8');

// We will add an assertion right after we reach the Basics step
const searchStr = `// Step 0: Source -> Next
      await page.getByTestId('next-step-button').click()

      // Fill in too short Title`;

const replacementStr = `// Step 0: Source -> Next
      await page.getByTestId('next-step-button').click()

      // Verify empty fields show required guidance, not "Looking good! ✨"
      await expect(page.getByText('Required. Minimum 3 characters.')).toBeVisible()
      await expect(page.getByText('Required. Explain your project (min 30 chars, max 1500 chars).')).toBeVisible()

      // Fill in too short Title`;

content = content.replace(searchStr, replacementStr);
fs.writeFileSync(file, content, 'utf8');
