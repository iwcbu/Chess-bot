import type { Route } from "./+types/about";
import AboutPage from '../../components/AboutPage/AboutPage'


export function meta({}: Route.MetaArgs) {
  return [
    { title: "Testing" },
    { name: "Damn" },
  ];
}

export default function About() {
  return (

    <AboutPage />

  )
}