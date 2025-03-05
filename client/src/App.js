import "bootstrap/dist/css/bootstrap.min.css";
import React from "react";
import "./App.css";
import ShoppingCart from "./components/SC/ShoppingCart";
import NavBar from "./components/NavBar/NavBar";
import Home from "./components/Home/Home";
import { Routes, Route, useNavigate } from "react-router-dom";
import Demo from "./components/Demo/Demo";
import LoginForm from "./components/Signup/LoginForm";
import { useDispatch } from "react-redux";
import PreviousOrders from "./PreviousOrders/PreviousOrders";

const mockUserData = [
  {
    username: "Narendra",
    email: "r@g.com",
    password: "RB",
    cart: [],
  },
  {
    username: "Karthik",
    email: "alladikarthik02@gmail.com",
    password: "alladi",
    cart: [],
  },
  {
    username: "Sashank",
    email: "sashank.desu@gmail.com",
    password: "sashankd",
    cart: [],
  },
];

const App = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const signInHandler = (details) => {
    for (let i of mockUserData) {
      if (i.email === details.email && i.password === details.password) {
        localStorage.setItem("username", i.username);
        dispatch({ type: "login", value: i });
        console.log("Logged in");
        navigate("/");
      }
    }
  };

  return (
    <div>
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} exact />
        <Route path="/cart" element={<ShoppingCart />} exact />
        <Route
          path="/signin"
          element={<LoginForm onSignin={signInHandler} />}
          exact
        />
        <Route path="/previous-items" element={<PreviousOrders />} exact />
        <Route
          path="/add-product/:id"
          element={<Demo />}
          exact
        />
      </Routes>
    </div>
  );
};

export default App;
