import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

// ...existing code...
import Game from "./app.js";
// ...existing code...

const root = createRoot(document.getElementById("root"));
root.render(
  <StrictMode>
    <Game />
  </StrictMode>
);
// ...existing code...