// frontend/app/routes.ts

import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/game.tsx"),
    route("about", "routes/about.tsx"),

] satisfies RouteConfig;
