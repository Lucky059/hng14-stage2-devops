const express = require("express");
const axios = require("axios"); // You'll need to add this to package.json
const app = express();

const API_URL = process.env.API_URL || "http://api:8000";

app.get("/", (req, res) => {
  res.send("Welcome to the HNG Stage 2 Frontend!");
});

// BUG FIX: Added route to actually test the microservice connection
app.get("/job-status/:id", async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`);
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: "Could not reach API", details: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, "0.0.0.0", () => { // Requirement: Bind to 0.0.0.0
  console.log(`Frontend running on port ${PORT}`);
});
