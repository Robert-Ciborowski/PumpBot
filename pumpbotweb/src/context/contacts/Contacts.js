import React, { Fragment, useContext, useEffect } from "react";
import ContactContext from "../../context/contact/contactContext";
import ContactItem from "./ContactItem";
import Spinner from "../../components/layout/Spinner";
import Pusher from "pusher-js";

export const Contacts = () => {
  const contactContext = useContext(ContactContext);
  Pusher.logToConsole = true;
  const pusher = new Pusher(`${process.env.PUSHER_ID}`, {
    cluster: "us2",
    forceTLS: true,
  });

  const { contacts, filtered, getData, loading, addContact } = contactContext;

  useEffect(() => {
    getData();
  }, []);

  if (contacts.length !== null && contacts.length === 0) {
    return <h4>No Data</h4>;
  }

  const channel = pusher.subscribe("my-channel");
  channel.bind("my-event", function (data) {
    getData();
  });

  if (loading) {
    return <Spinner />;
  } else {
    return (
      <Fragment>
        {filtered !== null
          ? filtered.map((contact) => (
              <ContactItem contact={contact} key={contact.id} />
            ))
          : contacts.map((contact) => (
              <ContactItem key={contact.id} contact={contact} />
            ))}
      </Fragment>
    );
  }
};

export default Contacts;
