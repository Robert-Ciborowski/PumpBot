import React from "react";
import Contacts from "../../context/contacts/Contacts";
import ContactFilter from "../../context/contacts/ContactFilter";
import HomeShowcase from "../layout/Navbar";

export const Home = () => {
  return (
    <div>
      <div className="container">
        <div className="row" style={{ marginTop: "75px" }}>
          <ContactFilter />
          <br />

          <Contacts />
        </div>
      </div>
    </div>
  );
};

export default Home;
