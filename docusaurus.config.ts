// @ts-check
const { themes: prismThemes } = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A comprehensive textbook on humanoid robotics and embodied AI',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://growwidtalha.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/humanoid-robotics-ebook',

  // GitHub pages deployment config.
  organizationName: 'GrowWidTalha', // Usually your GitHub org/user name.
  projectName: 'humanoid-robots-book', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // Custom fields for chatbot API configuration
  customFields: {
    chatbotApiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/', // Serve docs from the root
          sidebarPath: require.resolve('./sidebars.ts'),
          editUrl: "https://github.com/GrowWidTalha/humanoid-robotics-ebook/tree/main",
          // Removed invalid "markdown" option
          // Removed homePageId as it's deprecated
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Humanoid Robotics Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'modulesSidebar',
            position: 'left',
            label: 'Modules',
          },
          {
            to: '/auth/login',
            label: 'Login',
            position: 'right',
          },
          {
            to: '/auth/signup',
            label: 'Sign Up',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Modules',
            items: [
              {
                label: 'Module 1: ROS 2 Fundamentals',
                to: '/module1-ros2',
              },
              {
                label: 'Module 2: Digital Twin',
                to: '/module-02-digital-twin',
              },
              {
                label: 'Module 3: AI Robot Brain',
                to: '/module-3-ai-robot-brain/overview',
              },
              {
                label: 'Module 4: Vision-Language-Action',
                to: '/module-4-vla',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'yaml', 'json'],
      },
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: false,
        respectPrefersColorScheme: false,
      },
    }),
};

module.exports = config;
