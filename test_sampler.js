const assert = require("assert");

// This mirrors the processSample function in sampler_server.js
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

    const avg = valid.reduce((sum, v) => sum + v, 0) / valid.length;

    return {
        status: "ok",
        timestamp: data.timestamp,
        sampled_voltage: avg,
        sensors_used: valid.length
    };
}

// Test 1: Basic averaging 
const voltages = [120, 130, 140];
let result = processSample({ timestamp: 12345, voltage: voltages });
const avg = voltages.reduce((a, b) => a + b) / voltages.length;
assert(result.sampled_voltage === avg);
console.log("Basic averaging test passed");

// Test 2: Empty voltage array 
const emptySample = { timestamp: 12345, voltage: [] };
result = processSample(emptySample);
assert(result.status === "error");
console.log("Empty array test passed");

// Test 3: All invalid voltages 
const invalidSample = { timestamp: 12345, voltage: [50, 80, 220] };
result = processSample(invalidSample);
assert(result.status === "error");
console.log("All invalid voltages test passed");