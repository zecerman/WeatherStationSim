const express = require("express");

const app = express();
app.use(express.json());

function processSample(data) {

    if (!data.voltage || !Array.isArray(data.voltage)) {
        throw new Error("Invalid sample format");
    }

    const voltages = data.voltage;

    const valid = voltages.filter(v => v >= 90 && v <= 200);

    if (valid.length === 0) {
        return {
            status: "error",
            message: "No valid sensor readings"
        };
    }

    const avg =
        valid.reduce((sum, v) => sum + v, 0) / valid.length;

    return {
        status: "ok",
        timestamp: data.timestamp,
        sampled_voltage: avg,
        sensors_used: valid.length
    };
}

app.post("/sample", (req, res) => {
    try {
        const result = processSample(req.body);
        res.json(result);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

const PORT = 3000;

app.listen(PORT, () => {
    console.log(`Sampler running on port ${PORT}`);
});