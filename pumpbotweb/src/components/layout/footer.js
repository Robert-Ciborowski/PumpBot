import React from "react";
import { Link } from "react-router-dom";

export const Footer = () => {
  return (
    <footer id="footer" className="page-footer deep-purple lighten-1">
      <div className="container">
        <div className="row">
          <div className="col l6 s12">
            <h5 className="white-text">About Us</h5>
            <p className="grey-text text-lighten-4">
              PumpBot is made by a team of three passionate computer science
              students from the University of Toronto and Ryerson University. We
              strive to push the boundaries of machine learning by implementing
              it into new fields, such as criminology. We believe that machine
              learning technologies should be used for the good of humanity,
              which is why PumpBot serves to warn others about fraudulent pump &
              dump schemes.
            </p>
          </div>
          <div className="col l4 offset-l2 s12">
            <h5 className="white-text">Links to find us</h5>
            <ul>
              <li>
                <a
                  className="grey-text text-lighten-3"
                  href="https://github.com/jamestang12"
                >
                  James Tang
                </a>
              </li>
              <li>
                <a
                  className="grey-text text-lighten-3"
                  href="https://github.com/Robert-Ciborowski"
                >
                  Robert Ciborowski
                </a>
              </li>
              <li>
                <a
                  className="grey-text text-lighten-3"
                  href="https://github.com/Derek-Y-Wang"
                >
                  Derek Wang
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div className="footer-copyright deep-purple darken-1">
        <div className="container">
          PumpBot &copy; 2020
          <a className="grey-text text-lighten-4 right" href="#!"></a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
