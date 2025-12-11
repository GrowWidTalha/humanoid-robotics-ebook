// src/custom.d.ts
declare module '@docusaurus/types' {
  interface ThemeConfig {
    customFields?: { [key: string]: any };
  }
}
