const User = require("../models/User");

module.exports = async function (req, res, next) {
  let id = req.params.id;

  try {
    const user = await User.findById(id);
    if (!user) {
      return res.status(401).send("error");
    }
    next();
  } catch (error) {
    return res.status(500).send("error");
  }
};
