const express = require("express");
const router = express.Router();
const User = require("../models/User");
const Data = require("../models/Data");
const { check, validationResult } = require("express-validator");
const bcrypt = require("bcryptjs");
//const auth = require("../middleware/auth");

//@route GET api/pumpbot
//@desc Fetch data from database
router.get("/", async (req, res) => {
  try {
    const data = await Data.find();
    res.status(200).json(data);
  } catch (err) {
    return res.status(500).json({ errors: "Server error" });
  }
});

//@route POST api/pumpbot
//@desc Upload Data
router.post(
  "/",
  [
    check("email", "Please enter email").not().isEmpty(),
    check("password", "Please endter password").not().isEmpty(),
  ],
  async (req, res) => {
    const errros = validationResult(req);
    if (!errros.isEmpty()) {
      return res.status(400).json({ errros: errros.array() });
    }

    const { name, data, date, email, password } = req.body;
    try {
      let user = await User.findOne({ email: email });
      if (!user) {
        return res.status(400).json({ msg: "Invalid Credentails" });
      }

      const isMatch = await bcrypt.compare(password, user.password);
      if (!isMatch) {
        return res.status(400).json({ msg: "Invalid Credentails" });
      }

      if (user.role !== "admin") {
        return res.status(401).json({ msg: "Not authorized" });
      }

      const newData = new Data({
        date,
        data,
        name,
      });

      await newData.save();
      return res.status(200).json({ msg: newData });
    } catch (error) {
      return res.status(500).json({ errors: "Server error" });
    }
  }
);

module.exports = router;
