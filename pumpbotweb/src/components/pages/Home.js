import React from "react";
import Contacts from "../../context/contacts/Contacts";
import ContactFilter from "../../context/contacts/ContactFilter";

export const Home = () => {
  return (
    <div className="container">
      <div className="row" style={{ marginTop: "75px" }}>
        <ContactFilter />
        <br />

        <Contacts />
      </div>
    </div>
  );
};

export default Home;
