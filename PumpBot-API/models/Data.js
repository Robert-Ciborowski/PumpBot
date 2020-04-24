const mongoose = require("mongoose");

const DataSchema = mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  data: {
    type: String,
    required: true,
  },
  date: {
    type: String,
    required: true,
  },
});

module.exports = mongoose.model("data", DataSchema);
