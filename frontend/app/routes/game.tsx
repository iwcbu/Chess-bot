import type { Route } from "./+types/game";
import GamePage from '../../components/GamePage/GamePage'


export function meta({}: Route.MetaArgs) {
  return [
    { title: "MCB Game" },
    { name: "Games" },
  ];
}

export default function About() {
  return (
    <GamePage />
  )
}