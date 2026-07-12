import type { Route } from "./+types/game";
import GamePage from '../../components/GamePage/GamePage'


export function meta({}: Route.MetaArgs) {
  return [
    { title: "Play Chess | MyChessBot" },
    { 
      name: "description", 
      content:
        "Play against MyChessBot, a chess engine with multiple difficulty levels and move search logic."
    },
  ];
}

export default function About() {
  return (
    <GamePage />
  )
}