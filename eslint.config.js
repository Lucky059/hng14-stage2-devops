// eslint.config.js
const js = require("@eslint/js");

module.exports = [
  js.configs.recommended,
  {
    files: [
      "frontend/**/*.js",
      "app.js"
    ],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "commonjs"
    },
    env: {
      node: true
    },
    rules: {
      "no-unused-vars": "warn",
      "no-console": "off"
    }
  }
];

