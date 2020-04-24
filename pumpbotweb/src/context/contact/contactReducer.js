import {
  SET_LOADING,
  GET_CONTACT,
  FILTER_CONTACTS,
  CLEAR_FILTER,
  ADD_CONTACT,
} from "../types";

export default (state, action) => {
  switch (action.type) {
    case FILTER_CONTACTS:
      return {
        ...state,
        filtered: state.contacts.filter((contact) => {
          const regex = new RegExp(`${action.payload}`, "gi");
          return contact.name.match(regex) || contact.data.match(regex);
        }),
      };
    case CLEAR_FILTER:
      return {
        ...state,
        filtered: null,
      };
    case GET_CONTACT:
      return {
        ...state,
        contacts: action.payload,
        loading: false,
      };
    case ADD_CONTACT:
      return {
        ...state,
        contacts: [...state.contacts, action.payload],
      };
    default:
      return state;
  }
};
