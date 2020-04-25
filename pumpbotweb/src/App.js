import React, { useEffect, Fragment } from "react";
import M from "materialize-css/dist/js/materialize.min.js";
import "./App.css";
import "materialize-css/dist/css/materialize.min.css";
import ContactState from "./context/contact/ContactState";

import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Navbar from "./components/layout/Navbar";
import Home from "./components/pages/Home";
import About from "./components/pages/About";
import Footer from "./components/layout/footer";

function App() {
  useEffect(() => {
    //Init Materialize JS
    M.AutoInit();
  });
  return (
    <ContactState>
      <Router>
        <Navbar />
        <Switch>
          <Route exact path="/" component={Home} />
          <Route exact path="/about" component={About} />
        </Switch>
        <Footer />
      </Router>
    </ContactState>
  );
}

export default App;
