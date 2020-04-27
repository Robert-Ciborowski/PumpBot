import React, { useContext } from "react";
import { Link } from "react-router-dom";
import FadeIn from "react-fade-in";
import ContactContext from "../../context/contact/contactContext";

export const Navbar = () => {
  const contactContext = useContext(ContactContext);
  const { page, setPage } = contactContext;

  const onClick = (e) => {
    if (page === "home") {
      setPage("about");
    } else if (page === "about") {
      setPage("home");
    }
  };

  const homeBtn = (
    <Link
      to="/about"
      style={{ width: "200px" }}
      className="btn btn-large white purple-text "
      onClick={onClick}
    >
      LEARN MORE
    </Link>
  );

  const aboutBtn = (
    <Link
      to="/"
      style={{ width: "200px" }}
      className="btn btn-large white purple-text "
      onClick={onClick}
    >
      HOME
    </Link>
  );

  return (
    <header className="main-header">
      <nav className="transparent">
        <div className="container">
          <div className="nav-wrapper">
            <Link to="/" className="brand-logo">
              Pump Bot
            </Link>
          </div>
        </div>
        <FadeIn>
          <div className="showcase container">
            <div className="row">
              <div className="col s12 m10 offset-m1 center">
                <h5>Welcome To Pump Bot</h5>
                <br />

                <h1>Plan The Future</h1>
                <p>With Pump Bot The Future Is Within Your Control </p>
                <br />
                {page === "home" ? homeBtn : aboutBtn}
                <a
                  href="#footer"
                  style={{ width: "200px" }}
                  className="btn btn-large purple white-text"
                >
                  About Us
                </a>
              </div>
            </div>
          </div>
        </FadeIn>
      </nav>
    </header>
  );
};

export default Navbar;
