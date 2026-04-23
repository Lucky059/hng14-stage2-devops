// eslint.config.js
const js = require("@eslint/js");

module.exports = [
  {
    files: ["**/*.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "commonjs",
      globals: {
        require: "readonly",
        module: "readonly",
        __dirname: "readonly",
        console: "readonly",
        process: "readonly"
      }
    },
    rules: {
      ...js.configs.recommended.rules,
      "no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
    }
  }
];
