const express = require("express");
const router = express.Router();
const { check, validationResult } = require("express-validator");
const User = require("../models/User");
const bcrypt = require("bcryptjs");
const uuid = require("uuid");

//@route POST api/pumpbot/users
//@desc Created user
router.post(
  "/",
  [
    check("name", "Please add name").not().isEmpty(),
    check("email", "Please add email").isEmail(),
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { name, email, role, password } = req.body;
    const userId = uuid.v4();
    try {
      let user = await User.findOne({ email: email });
      if (user) {
        return res.status(400).json({ msg: "User already exists" });
      }

      user = new User({
        name,
        email,
        role,
        password,
      });

      const salt = await bcrypt.genSalt(10);

      user.password = await bcrypt.hash(password, salt);

      await user.save();
      return res.status(200).json({ msg: "User created" });
    } catch (error) {
      console.log(error);

      return res.status(500).json({ errors: "Server error" });
    }
  }
);

module.exports = router;
