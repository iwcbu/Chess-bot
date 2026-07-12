import type { Route } from "./+types/about";
import AboutPage from '../../components/AboutPage/AboutPage'


export function meta({}: Route.MetaArgs) {
  return [
    { title: "About | MyChessBot" },
    { 
      name: "description",
      content: 
        "Learn about MyChessBot, a portfolio chess engine project built with python-chess, React and FastAPI."
    },
  ];
}

export default function About() {
  return (

    <AboutPage />

  )
}