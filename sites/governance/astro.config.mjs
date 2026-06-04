import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Version is read from the committed VERSION file in this site
// directory. The Header component in @aegis-initiative/design-system
// reads `import.meta.env.AEGIS_VERSION`, which is populated here
// before Astro/Vite loads its env files.
const __dirname = path.dirname(fileURLToPath(import.meta.url));
process.env.AEGIS_VERSION = fs.readFileSync(path.resolve(__dirname, 'VERSION'), 'utf8').trim();

export default defineConfig({
  site: 'https://aegis-governance.com',
  integrations: [sitemap()],
  markdown: {
    shikiConfig: {
      theme: 'github-dark-default',
    },
  },
});
