// app/root.tsx
import { Outlet, Links, Meta, Scripts } from "react-router";
import NavBar from '../components/NavBar/NavBar';
import "./app.css"

export default function App() {
  return (
    <html>
      <head>
        <Meta />
        <Links />
      </head>
      <body>
        <NavBar />
        <Outlet />
        <Scripts />
      </body>
    </html>
  );
}
