import React from "react";
import { Link } from "react-router-dom";

export const Footer = () => {
  return (
    <footer className="page-footer deep-purple lighten-1">
      <div className="container">
        <div className="row">
          <div className="col l6 s12">
            <h5 className="white-text">About Us</h5>
            <p className="grey-text text-lighten-4">
              Lorem ipsum dolor sit amet, consectetur Lorem ipsum dolor sit
              amet, consectetur
            </p>
          </div>
          <div className="col l4 offset-l2 s12">
            <h5 className="white-text">Links</h5>
            <ul>
              <li>
                <a className="grey-text text-lighten-3" href="#!">
                  James
                </a>
              </li>
              <li>
                <a className="grey-text text-lighten-3" href="#!">
                  Robert
                </a>
              </li>
              <li>
                <a className="grey-text text-lighten-3" href="#!">
                  Derek
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div className="footer-copyright deep-purple darken-1">
        <div className="container">
          SpaceJack &copy; 2020
          <a className="grey-text text-lighten-4 right" href="#!">
            Terms & Conditionss
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
