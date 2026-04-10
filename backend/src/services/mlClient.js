const axios = require("axios");

async function rankWithML(payload) {
  const baseUrl = process.env.ML_SERVICE_URL || "http://localhost:5001";
  const response = await axios.post(`${baseUrl}/rank`, payload, {
    timeout: 6000,
  });

  return response.data;
}

module.exports = { rankWithML };
