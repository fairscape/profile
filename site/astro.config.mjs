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
      components: {
        SiteTitle: './src/components/SiteTitle.astro',
        PageSidebar: './src/components/PageSidebar.astro',
      },
      sidebar: [
        { label: 'Overview', link: '/' },
        {
          label: 'v0.2 (Current)',
          items: [
            { label: 'Specification', link: '/0.2/' },
            { label: 'Validation Rules (SHACL)', link: '/0.2/validation/' },
            { label: 'Croissant Mapping', link: '/0.2/croissant-mapping/' },
            { label: 'JSON Schemas', link: '/0.2/schemas/' },
          ],
        },
        {
          label: 'v0.1 (Superseded)',
          items: [
            { label: 'Specification', link: '/0.1/' },
            { label: 'Croissant Mapping', link: '/0.1/croissant-mapping/' },
            { label: 'JSON Schemas', link: '/0.1/schemas/' },
          ],
        },
        {
          label: 'Resources',
          items: [
            { label: 'Profile Crate (JSON-LD)', link: '/0.2/ro-crate-metadata.json' },
            { label: 'SHACL Shapes (TTL)', link: '/0.2/fairscape-shapes.ttl' },
            { label: 'EVI Vocabulary (TTL)', link: '/0.2/evi-vocabulary.ttl' },
            { label: 'Fairscape on GitHub', link: 'https://github.com/fairscape' },
          ],
        },
      ],
    }),
  ],
});
