import React, { useReducer } from "react";
import ContactContext from "./contactContext";
import contactReducer from "./contactReducer";
import axios from "axios";

import {
  GET_CONTACT,
  FILTER_CONTACTS,
  CLEAR_FILTER,
  ADD_CONTACT,
  SET_PAGE,
} from "../types";

const ContactState = (props) => {
  const initialState = {
    contacts: [
      {
        name: "James",
        data: "data",
        date: "date",
      },
    ],
    filtered: null,
    loading: true,
    page: "home",
  };

  const [state, dispatch] = useReducer(contactReducer, initialState);

  //Add Contact
  const addContact = (data) => {
    dispatch({ type: ADD_CONTACT, payload: data });
  };

  //Filter Contacts
  const filterContacts = (text) => {
    dispatch({ type: FILTER_CONTACTS, payload: text });
  };

  //Clear Filter
  const clearFilter = () => {
    dispatch({ type: CLEAR_FILTER });
  };

  //Get Data
  const getData = async () => {
    try {
      const res = await axios.get(
        "https://cors-anywhere.herokuapp.com/http://165.22.236.136:5000/api/pumpbot"
      );
      console.log(res.data.data);

      dispatch({
        type: GET_CONTACT,
        payload: res.data.data,
      });
    } catch (error) {
      console.log(error);
    }
  };

  const setPage = (flag) => {
    if (flag === "home") {
      dispatch({
        type: SET_PAGE,
        payload: "home",
      });
    } else {
      dispatch({
        type: SET_PAGE,
        payload: "about",
      });
    }
  };

  return (
    <ContactContext.Provider
      value={{
        contacts: state.contacts,
        filtered: state.filtered,
        loading: state.loading,
        page: state.page,
        setPage,
        clearFilter,
        filterContacts,
        getData,
        addContact,
      }}
    >
      {props.children}
    </ContactContext.Provider>
  );
};

export default ContactState;
