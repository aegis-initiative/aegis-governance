import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readSiteVersion } from '@aegis-initiative/design-system/build';

// Version is read from the committed VERSION file in this site
// directory. The Header component in @aegis-initiative/design-system
// reads `import.meta.env.AEGIS_VERSION`, which is populated here
// before Astro/Vite loads its env files. The VERSION file is JSON
// ({ tag, commit, released_at }); readSiteVersion() returns the tag.
const __dirname = path.dirname(fileURLToPath(import.meta.url));
process.env.AEGIS_VERSION = readSiteVersion({ cwd: __dirname });

export default defineConfig({
  site: 'https://aegis-governance.com',
  integrations: [sitemap()],
  markdown: {
    shikiConfig: {
      theme: 'github-dark-default',
    },
  },
});
