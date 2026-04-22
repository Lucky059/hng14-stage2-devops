// frontend/app.js
const express = require("express");

const app = express();

// Root route
app.get("/", (req, res) => {
  res.send("Welcome to the frontend!");
});

// Data route with proper error handling (uses next)
app.get("/data", async (req, res, next) => {
  try {
    const data = { message: "Sample data" };
    res.json(data);
  } catch (err) {
    console.error("Error in /data route:", err);
    next(err);
  }
});

// Info route (no next)
app.get("/info", (req, res) => {
  res.send("Info page");
});

// Global error handler
// We use _next because Express requires 4 arguments for error middleware
app.use((err, req, res, _next) => {
  console.error("Unhandled error:", err);
  res.status(500).send("Internal Server Error");
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Frontend running on port ${PORT}`);
});


