const mongoose = require("mongoose");

const DataSchema = mongoose.Schema({
  data_1: {
    type: String,
    default: undefined,
  },
  data_2: {
    type: String,
    default: undefined,
  },
  data_3: {
    type: String,
    default: undefined,
  },
  data_4: {
    type: String,
    default: undefined,
  },
  name: {
    type: String,
    default: undefined,
  },
});

module.exports = mongoose.model("data", DataSchema);
