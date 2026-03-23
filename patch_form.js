const fs = require('fs')
const file = 'components/ui/submit-project-form.tsx'
let content = fs.readFileSync(file, 'utf8')

// Title helper
content = content.replace(
  '<p className="form-helper-text mt-1 text-xs">Gunakan nama project yang singkat dan jelas.</p>',
  `<p className="form-helper-text mt-1 text-xs">
    {title.trim().length === 0
      ? \`Required. Minimum \${MIN_TITLE_LENGTH} characters.\`
      : title.trim().length < MIN_TITLE_LENGTH
        ? \`Needs \${MIN_TITLE_LENGTH - title.trim().length} more characters.\`
        : title.length > MAX_TITLE_LENGTH
          ? \`Exceeds maximum \${MAX_TITLE_LENGTH} characters.\`
          : 'Looking good! ✨'}
  </p>`,
)

// Tagline helper
content = content.replace(
  '<p className="form-helper-text mt-1 text-xs">\n                    Tagline singkat yang describe project lo dalam satu kalimat! ✨\n                  </p>',
  `<p className="form-helper-text mt-1 text-xs">
    {tagline.trim().length === 0
      ? \`Optional. At least \${MIN_TAGLINE_LENGTH} characters if provided.\`
      : tagline.trim().length < MIN_TAGLINE_LENGTH
        ? \`Needs \${MIN_TAGLINE_LENGTH - tagline.trim().length} more characters.\`
        : tagline.length > MAX_TAGLINE_LENGTH
          ? \`Exceeds maximum \${MAX_TAGLINE_LENGTH} characters.\`
          : 'Looking good! ✨'}
  </p>`,
)

// Description helper
content = content.replace(
  `{description.trim().length > 0 && description.trim().length < MIN_DESCRIPTION_LENGTH\n                      ? \`Minimum \${MIN_DESCRIPTION_LENGTH} karakter yang bermakna untuk menjelaskan project ini.\`\n                      : 'Looking good! ✨'}`,
  `{description.trim().length === 0
    ? \`Required. Explain your project (min \${MIN_DESCRIPTION_LENGTH} chars, max \${MAX_DESCRIPTION_LENGTH} chars).\`
    : description.trim().length < MIN_DESCRIPTION_LENGTH
      ? \`Needs \${MIN_DESCRIPTION_LENGTH - description.trim().length} more characters to reach the \${MIN_DESCRIPTION_LENGTH} minimum.\`
      : description.length > MAX_DESCRIPTION_LENGTH
        ? \`Exceeds maximum \${MAX_DESCRIPTION_LENGTH} characters.\`
        : 'Looking good! ✨'}`,
)

// Category helper - we should probably add a helper if missing
// wait, category helper:
// {category && categories.find((c) => c.name === category)?.description && (
//   <p className="form-helper-text mt-1 text-xs text-muted-foreground">
//     {categories.find((c) => c.name === category)?.description}
//   </p>
// )}

fs.writeFileSync(file, content, 'utf8')
