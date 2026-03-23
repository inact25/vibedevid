const fs = require('fs')
const file = 'components/ui/submit-project-form.tsx'
let content = fs.readFileSync(file, 'utf8')

// The original chunk is:
/*
                {category && categories.find((c) => c.name === category)?.description && (
                  <p className="form-helper-text mt-1 text-xs text-muted-foreground">
                    {categories.find((c) => c.name === category)?.description}
                  </p>
                )}
*/

content = content.replace(
  `{category && categories.find((c) => c.name === category)?.description && (
                  <p className="form-helper-text mt-1 text-xs text-muted-foreground">
                    {categories.find((c) => c.name === category)?.description}
                  </p>
                )}`,
  `<p className="form-helper-text mt-1 text-xs text-muted-foreground">
                  {!category 
                    ? 'Required. Select a category that best fits your project.' 
                    : categories.find((c) => c.name === category)?.description || 'Looking good! ✨'}
                </p>`,
)

fs.writeFileSync(file, content, 'utf8')
