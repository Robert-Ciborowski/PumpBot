const express = require("express");
const connectDB = require("./config/db");

const app = express();

//Connect Database
connectDB();

//Init Middleware
app.use(express.json({ extended: false }));

//Set up route
app.get("/", (req, res) => res.json({ msg: "Welcome to the PumpBot API" }));

//Define Routes
app.use("/api/pumpbot", require("./routes/data"));
app.use("/api/pumpbot/users", require("./routes/users"));

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
