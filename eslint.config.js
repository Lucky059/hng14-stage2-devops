import js from "@eslint/js";

export default [
  js.configs.recommended,
  {
    files: ["frontend/**/*.js", "views/**/*.js", "app.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
    },
    rules: {
      // Add or override rules here
      "no-unused-vars": "warn",
      "no-console": "off",
    },
  },
];
