// frontend/components/AboutPage/AboutPage.tsx

import styles from "./AboutPage.module.css";

const chapters = [
    {
    move: "1. e4",
    label: "Opening",
    title: "Project Overview",
    meta: "candidate move",
    eval: "+0.3",
    body: "MyChessBot is a software engineering portfolio project centered around building a playable chess AI from the ground up. The app combines a React interface with a FastAPI backend layer, turning each move into both a game decision and a structured software event. Player input is validated, board state is evaluated, and the engine responds through a recusive decision making process designed to model how a chess bot thinks.",
    notes: ["chess AI project", "engine gameplay design", "state based architecture"],
  },
  {
    move: "2. Nf3",
    label: "The Position",
    title: "How It Works",
    meta: "position analysis",
    eval: "depth=2",
    body: "The frontend renders the current position using data from the backend, including FEN, legal moves, turn state, game status, and the last move played. When a player submits a move, the API validates the UCI notation, updates the board, and returns a new position. This creates a clean feedback loop between interface, rules engine, and AI decision logic.",
    notes: ["FEN translated UI", "validated move pipeline", "API controlled game state"],
  },
  {
    move: "3. Bb5",
    label: "The Engine",
    title: "Key Features",
    meta: "evaluation",
    eval: "+0.7",
    body: "The bot supports multiple levels of decision-making, from simple legal move selection to game state evaluation and deeper minimax-style search. The engine considers board state, material balance, legal responses, and future move possibilities, while the interface adds animated feedback, capture previews, undo/reset controls, and endgame result handling.",
    notes: ["AI move selection", "heuristic evaluation", "minimax search"],
  },
  {
    move: "4. O-O",
    label: "The Board",
    title: "Tech Stack",
    meta: "engine room",
    eval: "alpha-beta",
    body: "MyChessBot is built with React Router, TypeScript, CSS modules, and custom SVG chess assets on the frontend. The backend uses FastAPI and the python-chess library to manage rules, board state, legal move generation, and engine calculations. This separation keeps the UI focused on interaction while the backend handles the core game logic and AI behavior.",
    notes: ["React + TypeScript", "FastAPI engine layer", "python-chess rules"],
  },
  {
    move: "5. Re1",
    label: "The Search",
    title: "Development Process",
    meta: "search depth",
    eval: "depth=3",
    body: "The development process began with the core chess logic: validating legal moves, tracking board state, and returning clear game information from the backend. From there, I built FastAPI endpoints for player moves, bot moves, undo functionality, and game status updates. Once the API was in place, I connected the React frontend and refined the user experience around board interaction, difficulty selection, and game feedback. This project also gave me the opportunity to deepen my understanding of search algorithms, board evaluation, and full-stack application design. As the engine grew, I added move selection strategies, minimax search, alpha-beta pruning, and testing around the game logic to make the system more reliable.",
    notes: ["engine iteration", "API contracts", "search-based logic"],
  },
  {
    move: "6. Qh5+",
    label: "The Player",
    title: "About the Developer",
    meta: "final annotation",
    eval: "#",
    body: "I built MyChessBot as a Boston University computer science graduate interested in the intersection of algorithms, AI behavior, and interactive software. Chess has always appealed to me because it rewards pattern recognition, tactical planning, and thinking several moves ahead. What started as an effort to build a more challenging chess opponent became a full-stack engineering project focused on search algorithms, backend architecture, and thoughtful user experience.",
    notes: ["software engineering", "algorithmic thinking", "AI-inspired design"],
  }
];

const notation = ["e4", "Nf3", "Bb5", "O-O", "Re1", "Qh5+", "+0.7", "depth=3"];

export default function AboutPage() {
  return (
    <main className={styles.page}>
      <div className={styles.boardGhost} aria-hidden="true" />
      <div className={styles.notationField} aria-hidden="true">
        {notation.map((mark) => (
          <span key={mark}>{mark}</span>
        ))}
      </div>

      <section className={styles.hero}>
        <div className={styles.heroCopy}>
          <p className={styles.eyebrow}>Portfolio chess engine manuscript</p>
          <h1>MyChessBot</h1>
          <p>
            A modern chess bot told like an old strategy book: board geometry, notation, engine search, and interface craft
            layered into one playable full-stack experiment.
          </p>
        </div>
      </section>

      <section className={styles.timeline} aria-label="About MyChessBot sections">
        {chapters.map((chapter, index) => (
          <article className={styles.chapter} key={chapter.move}>
            <div className={styles.moveNumber}>
              <span>{chapter.move}</span>
            </div>

            <div className={styles.plate}>
              <div className={styles.sectionMeta}>
                <span>{chapter.label}</span>
                <span>{chapter.meta}</span>
                <span>{chapter.eval}</span>
              </div>
              <h2>{chapter.title}</h2>
              <p>{chapter.body}</p>
              <ul>
                {chapter.notes.map((note) => (
                  <li key={note}>{note}</li>
                ))}
              </ul>
            </div>

            <div className={styles.diagram} aria-hidden="true">
              {index === 1 || index === 3 || index === 4 ? (
                <div className={styles.searchTree}>
                  <span />
                  <span />
                  <span />
                  <span />
                  <span />
                  <span />
                </div>
              ) : (
                <div className={styles.annotation}>
                  <span>{chapter.move.split(" ")[1]}</span>
                  <span>{chapter.eval}</span>
                </div>
              )}
            </div>
          </article>
        ))}
      </section>
    </main>
  );
}
