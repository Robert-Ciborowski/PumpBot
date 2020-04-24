import React from "react";
import { Link } from "react-router-dom";
import FadeIn from "react-fade-in";

export const Navbar = () => {
  return (
    <header className="main-header">
      <nav className="transparent">
        <div className="container">
          <div className="nav-wrapper">
            <Link to="#!" className="brand-logo">
              Pump Bot
            </Link>
          </div>
        </div>
        <FadeIn>
          <div className="showcase container">
            <div className="row">
              <div className="col s12 m10 offset-m1 center">
                <h5>Welcome To Pump Bot</h5>
                <h1>Plan The Future</h1>
                <p>
                  lorem ipsum dolor sit amet, consecjkdljf dshfkjhds djs hfkjh
                  skjd hfs{" "}
                </p>
                <br />
                <Link
                  to="#!"
                  style={{ width: "200px" }}
                  className="btn btn-large white purple-text "
                >
                  LEARN MORE
                </Link>
                <Link
                  to="#!"
                  style={{ width: "200px" }}
                  className="btn btn-large purple white-text"
                >
                  About Us
                </Link>
              </div>
            </div>
          </div>
        </FadeIn>
      </nav>
    </header>
  );
};

export default Navbar;
