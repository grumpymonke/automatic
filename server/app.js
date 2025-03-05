const express = require("express");
const mongoose = require("mongoose");
const Order = require("./models/Order");
const dotenv =require("dotenv").config();

const app = express();
app.use(express.json());
const cors = require("cors");

app.use(cors());
mongoose.connect("mongodb+srv://manishvenkat303:<db_password>@cluster0.5dfku.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
  process.env.MONGO_URI,
  {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  }
);

// POST route to save an order
app.post("/models/Order", async (req, res) => {
  try {
    const order = new Order(req.body);
    await order.save();
    res.status(201).json({ message: "Order saved successfully" });
  } catch (error) {
    console.error("Failed to save order:", error);
    res.status(500).json({ message: "Failed to save order" });
  }
});

// GET route to fetch all orders
app.get("/models/Order", async (req, res) => {
  try {
    const orders = await Order.find();
    res.json(orders);
  } catch (error) {
    console.error("Failed to fetch orders:", error);
    res.status(500).json({ message: "Failed to fetch orders" });
  }
});

const port = 8080;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
