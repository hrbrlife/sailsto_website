import { defineConfig } from 'tinacms';

export default defineConfig({
  branch: 'main',
  build: { outputFolder: 'admin', publicFolder: 'static' },
  media: { tina: { mediaRoot: 'uploads', publicFolder: 'static' } },
  schema: {
    collections: [
      // ── MAIN PAGES ──────────────────────────────────────────────
      {
        name: 'page',
        label: 'Pages',
        path: 'content',
        match: { include: '*' },
        format: 'md',
        fields: [
          { type: 'string', name: 'title', label: 'Title', required: true },
          { type: 'string', name: 'description', label: 'Meta Description', ui: { component: 'textarea' } },
          { type: 'string', name: 'ogImage', label: 'OG Image' },
          { type: 'string', name: 'keywords', label: 'Keywords', list: true },
          { type: 'boolean', name: 'draft', label: 'Draft' },
          {
            type: 'string', name: 'stylesheets', label: 'Stylesheets', list: true,
            description: 'CSS files to include',
          },
          {
            type: 'string', name: 'scripts', label: 'Scripts', list: true,
            description: 'JS files to include',
          },
          {
            type: 'string', name: 'headScripts', label: 'Head Scripts', list: true,
            description: 'JS files to include in <head>',
          },
          { type: 'rich-text', name: 'body', label: 'Body', isBody: true },
        ],
      },

      // ── COMPANY PAGES ───────────────────────────────────────────
      {
        name: 'company',
        label: 'Company Pages',
        path: 'content/company',
        format: 'md',
        fields: [
          { type: 'string', name: 'title', label: 'Title', required: true },
          { type: 'string', name: 'description', label: 'Meta Description', ui: { component: 'textarea' } },
          { type: 'string', name: 'ogImage', label: 'OG Image' },
          { type: 'string', name: 'keywords', label: 'Keywords', list: true },
          { type: 'string', name: 'stylesheets', label: 'Stylesheets', list: true },
          { type: 'string', name: 'scripts', label: 'Scripts', list: true },
          { type: 'rich-text', name: 'body', label: 'Body', isBody: true },
        ],
      },

      // ── DOCUMENTATION ───────────────────────────────────────────
      {
        name: 'docs',
        label: 'Documentation',
        path: 'content/knowledge/docs',
        format: 'md',
        fields: [
          { type: 'string', name: 'title', label: 'Title', required: true },
          { type: 'string', name: 'description', label: 'Description', ui: { component: 'textarea' } },
          { type: 'string', name: 'ogImage', label: 'OG Image' },
          { type: 'string', name: 'keywords', label: 'Keywords', list: true },
          { type: 'boolean', name: 'draft', label: 'Draft' },
          { type: 'string', name: 'stylesheets', label: 'Stylesheets', list: true },
          { type: 'string', name: 'scripts', label: 'Scripts', list: true },
          { type: 'rich-text', name: 'body', label: 'Body', isBody: true },
        ],
      },

      // ── GUIDES ──────────────────────────────────────────────────
      {
        name: 'guides',
        label: 'Guides',
        path: 'content/knowledge/guides',
        format: 'md',
        fields: [
          { type: 'string', name: 'title', label: 'Title', required: true },
          { type: 'string', name: 'description', label: 'Description', ui: { component: 'textarea' } },
          { type: 'string', name: 'ogImage', label: 'OG Image' },
          { type: 'string', name: 'keywords', label: 'Keywords', list: true },
          { type: 'boolean', name: 'draft', label: 'Draft' },
          { type: 'string', name: 'stylesheets', label: 'Stylesheets', list: true },
          { type: 'string', name: 'scripts', label: 'Scripts', list: true },
          { type: 'rich-text', name: 'body', label: 'Body', isBody: true },
        ],
      },

      // ── GLOSSARY ────────────────────────────────────────────────
      {
        name: 'glossary',
        label: 'Glossary',
        path: 'content/knowledge/glossary',
        format: 'md',
        fields: [
          { type: 'string', name: 'title', label: 'Term', required: true },
          { type: 'string', name: 'short', label: 'Short Definition' },
          { type: 'string', name: 'description', label: 'Full Description', ui: { component: 'textarea' } },
          { type: 'string', name: 'keywords', label: 'Related Terms', list: true },
          { type: 'rich-text', name: 'body', label: 'Body', isBody: true },
        ],
      },

      // ── BLOG ────────────────────────────────────────────────────
      {
        name: 'blog',
        label: 'Blog Posts',
        path: 'content/knowledge/blog',
        format: 'md',
        fields: [
          { type: 'string', name: 'title', label: 'Title', required: true },
          { type: 'string', name: 'description', label: 'Description', ui: { component: 'textarea' } },
          { type: 'datetime', name: 'date', label: 'Date' },
          { type: 'string', name: 'author', label: 'Author' },
          { type: 'string', name: 'ogImage', label: 'OG Image' },
          { type: 'string', name: 'keywords', label: 'Tags', list: true },
          { type: 'boolean', name: 'draft', label: 'Draft' },
          { type: 'rich-text', name: 'body', label: 'Body', isBody: true },
        ],
      },

      // ── DATA: ROADMAP ───────────────────────────────────────────
      {
        name: 'roadmap',
        label: 'Roadmap',
        path: 'data',
        match: { include: 'roadmap' },
        format: 'yaml',
        fields: [
          { type: 'string', name: 'current_status', label: 'Current Status' },
          {
            type: 'object', name: 'current_status_label', label: 'Status Label',
            fields: [
              { type: 'string', name: 'en', label: 'English' },
              { type: 'string', name: 'fr', label: 'French' },
            ],
          },
          {
            type: 'object', name: 'hero', label: 'Hero',
            fields: [
              { type: 'string', name: 'en', label: 'English Title' },
              { type: 'string', name: 'fr', label: 'French Title' },
            ],
          },
        ],
      },

      // ── DATA: VERSION ───────────────────────────────────────────
      {
        name: 'version',
        label: 'Version Info',
        path: 'data',
        match: { include: 'version' },
        format: 'json',
        fields: [
          { type: 'string', name: 'hash', label: 'Git Hash' },
          { type: 'string', name: 'hashShort', label: 'Short Hash' },
          { type: 'string', name: 'date', label: 'Build Date' },
          { type: 'string', name: 'message', label: 'Message' },
          { type: 'string', name: 'tag', label: 'Tag' },
          { type: 'number', name: 'buildNumber', label: 'Build Number' },
        ],
      },
    ],
  },
});
