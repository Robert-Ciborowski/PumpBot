import React from "react";
import Fadein from "react-fade-in";
import FadeIn from "react-fade-in";

export const ContactItem = ({ contact }) => {
  const MAX_LENGTH = 110;

  return (
    <FadeIn>
      <div className="col m6 s12">
        <div className="card">
          <div className="card-content">
            <span className="card-title purple-text">{contact.name}</span>
            {contact.data.length > MAX_LENGTH ? (
              <p style={{ marginTop: "15px" }}>
                {`${contact.data.substring(0, MAX_LENGTH)}......`}
              </p>
            ) : (
              <p style={{ marginTop: "15px" }}>{contact.data} </p>
            )}
            <br />
            <a className="activator">Read More</a>
          </div>
          <div className="card-reveal">
            <span className="card-title">
              {contact.name}
              <i className="material-icons">close</i>
            </span>
            <p style={{ marginTop: "15px" }}>{contact.data}</p>
          </div>
          <div className="card-action">
            <span>Date: {contact.dateFormat}</span>
          </div>
        </div>
      </div>
    </FadeIn>
  );
};

export default ContactItem;
