import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://fairscape.github.io',
  base: '/profile',
  trailingSlash: 'ignore',
  integrations: [
    starlight({
      title: 'Fairscape Profile',
      description: 'Fairscape Release RO-Crate Profile specification.',
      social: {
        github: 'https://github.com/fairscape',
      },
      customCss: ['./src/styles/fairscape.css'],
      sidebar: [
        { label: 'Overview', link: '/' },
        {
          label: 'v0.1 (Current)',
          items: [
            { label: 'Specification', link: '/0.1/' },
            { label: 'Croissant Mapping', link: '/0.1/croissant-mapping/' },
            { label: 'JSON Schemas', link: '/0.1/schemas/' },
          ],
        },
        {
          label: 'Resources',
          items: [
            { label: 'Profile Crate (JSON-LD)', link: '/0.1/ro-crate-metadata.json' },
            { label: 'EVI Vocabulary (TTL)', link: '/0.1/evi-vocabulary.ttl' },
            { label: 'Fairscape on GitHub', link: 'https://github.com/fairscape' },
          ],
        },
      ],
    }),
  ],
});
