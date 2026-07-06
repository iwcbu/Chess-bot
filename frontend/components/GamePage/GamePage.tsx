// frontend/components/GamePage/GamePage.tsx

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { CSSProperties, FormEvent } from "react";
import {
  type Difficulty,
  type GameStatus,
  getGame,
  makeBotMove,
  makeMove,
  resetGame,
  undoMove,
} from "../../api/chessApi";
import styles from "./GamePage.module.css";

import blackBishop from "../../assets/black_bishop.svg";
import blackKing from "../../assets/black_king.svg";
import blackKnight from "../../assets/black_knight.svg";
import blackPawn from "../../assets/black_pawn.svg";
import blackQueen from "../../assets/black_queen.svg";
import blackRook from "../../assets/black_rook.svg";
import whiteBishop from "../../assets/white_bishop.svg";
import whiteKing from "../../assets/white_king.svg";
import whiteKnight from "../../assets/white_knight.svg";
import whitePawn from "../../assets/white_pawn.svg";
import whiteQueen from "../../assets/white_queen.svg";
import whiteRook from "../../assets/white_rook.svg";

type PieceSymbol = "p" | "n" | "b" | "r" | "q" | "k" | "P" | "N" | "B" | "R" | "Q" | "K";
type PieceColor = "white" | "black";
type PendingAction = "load" | "move" | "bot" | "undo" | "reset" | "refresh" | null;
type PieceAnimationStyle = CSSProperties & {
  "--move-x": number;
  "--move-y": number;
};

interface BoardPiece {
  symbol: PieceSymbol;
  color: PieceColor;
  name: string;
  image: string;
}

interface BoardSquare {
  id: string;
  file: string;
  rank: number;
  piece: BoardPiece | null;
  isLight: boolean;
}

interface PieceAnimation {
  key: number;
  to: string;
  deltaX: number;
  deltaY: number;
}

interface GameResult {
  title: string;
  subtitle: string;
}

const files = ["a", "b", "c", "d", "e", "f", "g", "h"];
const promotionPieces = ["q", "r", "b", "n"];
const difficulties: Difficulty[] = ["easy", "medium", "hard", "expert"];
const MOVE_ANIMATION_MS = 260;
const BOT_REPLY_DELAY_MS = 200;

const pieceImages: Record<PieceSymbol, string> = {
  p: blackPawn,
  n: blackKnight,
  b: blackBishop,
  r: blackRook,
  q: blackQueen,
  k: blackKing,
  P: whitePawn,
  N: whiteKnight,
  B: whiteBishop,
  R: whiteRook,
  Q: whiteQueen,
  K: whiteKing,
};

const pieceNames: Record<string, string> = {
  p: "pawn",
  n: "knight",
  b: "bishop",
  r: "rook",
  q: "queen",
  k: "king",
};

const statusLabels: Record<string, string> = {
  active: "Active",
  check: "Check",
  checkmate: "Checkmate",
  stalemate: "Stalemate",
  game_over: "Game over",
};

function isPieceSymbol(value: string): value is PieceSymbol {
  return value in pieceImages;
}

function createPiece(symbol: PieceSymbol): BoardPiece {
  const color = symbol === symbol.toUpperCase() ? "white" : "black";
  const name = `${color} ${pieceNames[symbol.toLowerCase()]}`;

  return {
    symbol,
    color,
    name,
    image: pieceImages[symbol],
  };
}

function parseFen(fen: string): BoardSquare[] {
  const boardFen = fen.split(" ")[0];
  const ranks = boardFen.split("/");
  const squares: BoardSquare[] = [];

  ranks.forEach((rankFen, rankIndex) => {
    let fileIndex = 0;
    const rank = 8 - rankIndex;

    for (const char of rankFen) {
      if (/\d/.test(char)) {
        const emptySquares = Number(char);
        for (let index = 0; index < emptySquares; index += 1) {
          const file = files[fileIndex];
          squares.push({
            id: `${file}${rank}`,
            file,
            rank,
            piece: null,
            isLight: (fileIndex + rankIndex) % 2 === 0,
          });
          fileIndex += 1;
        }
      } else if (isPieceSymbol(char)) {
        const file = files[fileIndex];
        squares.push({
          id: `${file}${rank}`,
          file,
          rank,
          piece: createPiece(char),
          isLight: (fileIndex + rankIndex) % 2 === 0,
        });
        fileIndex += 1;
      }
    }
  });

  return squares;
}

function formatMove(move: string | null) {
  if (!move) {
    return "None";
  }

  const promotion = move[4] ? `=${move[4].toUpperCase()}` : "";
  return `${move.slice(0, 2)} to ${move.slice(2, 4)}${promotion}`;
}

function getMoveForSquares(from: string, to: string, legalMoves: string[]) {
  const baseMove = `${from}${to}`;

  if (legalMoves.includes(baseMove)) {
    return baseMove;
  }

  return promotionPieces.map((piece) => `${baseMove}${piece}`).find((move) => legalMoves.includes(move)) ?? null;
}

function getSquarePosition(square: string) {
  const fileIndex = files.indexOf(square[0]);
  const rank = Number(square[1]);

  if (fileIndex === -1 || Number.isNaN(rank)) {
    return null;
  }

  return {
    column: fileIndex,
    row: 8 - rank,
  };
}

function getAnimationDelay() {
  if (typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return 0;
  }

  return MOVE_ANIMATION_MS + BOT_REPLY_DELAY_MS;
}

function wait(ms: number) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}

function getGameResult(game: GameStatus | null): GameResult | null {
  if (!game || game.status === "active" || game.status === "check") {
    return null;
  }

  if (game.status === "checkmate") {
    const winner = game.turn === "white" ? "black" : "white";

    if (winner === "white") {
      return {
        title: "You win!",
        subtitle: "Humanity prevails by checkmate.",
      };
    }

    return {
      title: "Bot wins",
      subtitle: "The machine wins by checkmate.",
    };
  }

  if (game.status === "stalemate") {
    return {
      title: "Draw",
      subtitle: "The match ends by stalemate.",
    };
  }

  return {
    title: "Game over",
    subtitle: "The match is complete.",
  };
}

export default function GamePage() {
  const [game, setGame] = useState<GameStatus | null>(null);
  const [selectedSquare, setSelectedSquare] = useState<string | null>(null);
  const [moveDraft, setMoveDraft] = useState("");
  const [difficulty, setDifficulty] = useState<Difficulty>("medium");
  const [opening, setOpening] = useState<string | null>(null);
  const [autoBot, setAutoBot] = useState(true);
  const [pendingAction, setPendingAction] = useState<PendingAction>("load");
  const [error, setError] = useState<string | null>(null);
  const [pieceAnimation, setPieceAnimation] = useState<PieceAnimation | null>(null);
  const animationKeyRef = useRef(0);

  const boardSquares = useMemo(() => (game ? parseFen(game.fen) : []), [game]);
  const selectedMoves = useMemo(
    () => (selectedSquare && game ? game.legal_moves.filter((move) => move.startsWith(selectedSquare)) : []),
    [game, selectedSquare],
  );
  const legalDestinations = useMemo(() => new Set(selectedMoves.map((move) => move.slice(2, 4))), [selectedMoves]);
  const captureDestinations = useMemo(() => {
    if (!selectedSquare) {
      return new Set<string>();
    }

    const selectedPiece = boardSquares.find((square) => square.id === selectedSquare)?.piece;
    const squareById = new Map(boardSquares.map((square) => [square.id, square]));

    return new Set(
      selectedMoves
        .map((move) => move.slice(2, 4))
        .filter((destination) => {
          const destinationPiece = squareById.get(destination)?.piece;
          return Boolean(selectedPiece && destinationPiece && destinationPiece.color !== selectedPiece.color);
        }),
    );
  }, [boardSquares, selectedMoves, selectedSquare]);
  const lastMoveSquares = useMemo(
    () => (game?.last_move ? new Set([game.last_move.slice(0, 2), game.last_move.slice(2, 4)]) : new Set<string>()),
    [game?.last_move],
  );

  const isBusy = pendingAction !== null;
  const isGameActive = game?.status === "active" || game?.status === "check";
  const gameResult = useMemo(() => getGameResult(game), [game]);

  const startPieceAnimation = useCallback((move: string | null | undefined) => {
    if (!move || move.length < 4) {
      setPieceAnimation(null);
      return;
    }

    const from = move.slice(0, 2);
    const to = move.slice(2, 4);
    const fromPosition = getSquarePosition(from);
    const toPosition = getSquarePosition(to);

    if (!fromPosition || !toPosition) {
      setPieceAnimation(null);
      return;
    }

    animationKeyRef.current += 1;
    setPieceAnimation({
      key: animationKeyRef.current,
      to,
      deltaX: fromPosition.column - toPosition.column,
      deltaY: fromPosition.row - toPosition.row,
    });
  }, []);

  const commitGame = useCallback(
    (nextGame: GameStatus, animatedMove?: string | null) => {
      startPieceAnimation(animatedMove);
      setGame(nextGame);
      setOpening(game?.bot_opening ?? null);
    },
    [startPieceAnimation],
  );

  const clearPieceAnimation = (animationKey: number) => {
    setPieceAnimation((currentAnimation) => (currentAnimation?.key === animationKey ? null : currentAnimation));
  };

  const loadGame = useCallback(async (action: PendingAction = "refresh") => {
    setPendingAction(action);
    setError(null);

    try {
      const currentGame = await getGame();
      commitGame(currentGame);
      setSelectedSquare(null);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not reach the chess API.");
    } finally {
      setPendingAction(null);
    }
  }, [commitGame]);

  useEffect(() => {
    void loadGame("load");
  }, [loadGame]);

  const runBotMove = useCallback(
    async (action: PendingAction = "bot") => {
      setPendingAction(action);
      setError(null);

      try {
        const nextGame = await makeBotMove(difficulty, opening);
        commitGame(nextGame, nextGame.last_move);
        setSelectedSquare(null);
      } catch (requestError) {
        setError(requestError instanceof Error ? requestError.message : "The bot could not make a move.");
      } finally {
        setPendingAction(null);
      }
    },
    [difficulty],
  );

  const submitMove = useCallback(
    async (move: string) => {
      const normalizedMove = move.trim().toLowerCase();

      if (!game || !normalizedMove || isBusy) {
        return;
      }

      if (!game.legal_moves.includes(normalizedMove)) {
        setError(`${normalizedMove} is not legal in this position.`);
        return;
      }

      setPendingAction("move");
      setError(null);

      try {
        const nextGame = await makeMove(normalizedMove);
        commitGame(nextGame, normalizedMove);
        setMoveDraft("");
        setSelectedSquare(null);

        if (autoBot && nextGame.turn === "black" && (nextGame.status === "active" || nextGame.status === "check")) {
          await wait(getAnimationDelay());
          setPendingAction("bot");
          const botGame = await makeBotMove(difficulty, opening);
          commitGame(botGame, botGame.last_move);
        }
      } catch (requestError) {
        setError(requestError instanceof Error ? requestError.message : "Could not make that move.");
      } finally {
        setPendingAction(null);
      }
    },
    [autoBot, difficulty, game, isBusy],
  );

  const handleSquareClick = (square: BoardSquare) => {
    if (!game || isBusy || !isGameActive) {
      return;
    }

    if (!selectedSquare) {
      if (square.piece?.color === game.turn) {
        setSelectedSquare(square.id);
        setError(null);
      }
      return;
    }

    if (square.id === selectedSquare) {
      setSelectedSquare(null);
      return;
    }

    const move = getMoveForSquares(selectedSquare, square.id, game.legal_moves);
    if (move) {
      void submitMove(move);
      return;
    }

    if (square.piece?.color === game.turn) {
      setSelectedSquare(square.id);
      setError(null);
      return;
    }

    setError(`${selectedSquare} to ${square.id} is not legal.`);
  };

  const handleMoveSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    void submitMove(moveDraft);
  };

  const handleUndo = async () => {
    setPendingAction("undo");
    setError(null);

    try {
      const nextGame = await undoMove();
      commitGame(nextGame);
      setSelectedSquare(null);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "There is no move to undo.");
    } finally {
      setPendingAction(null);
    }
  };

  const handleReset = async () => {
    setPendingAction("reset");
    setError(null);

    try {
      const nextGame = await resetGame();
      commitGame(nextGame);
      setSelectedSquare(null);
      setMoveDraft("");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not reset the game.");
    } finally {
      setPendingAction(null);
    }
  };

  return (
    <main className={styles.page}>
      <section className={styles.gameHeader}>
        <div>
          <p className={styles.eyebrow}>MyChessBot</p>
          <h1>Chess Lab</h1>
        </div>
        <div className={styles.statusGrid} aria-live="polite">
          <div>
            <span>Turn</span>
            <strong>{game ? game.turn : "..."}</strong>
          </div>
          <div>
            <span>Status</span>
            <strong>{game ? statusLabels[game.status] ?? game.status : "Loading"}</strong>
          </div>
          <div>
            <span>Last</span>
            <strong>{game ? formatMove(game.last_move) : "None"}</strong>
          </div>
        </div>
      </section>

      {error ? <div className={styles.errorBanner}>{error}</div> : null}

      <section className={styles.gameLayout}>
        <div className={styles.boardShell}>
          {game ? (
            <div className={styles.boardFrame}>
              <div className={[styles.chessboard, gameResult ? styles.finishedBoard : ""].join(" ")} aria-label="Chess board">
                {boardSquares.map((square) => {
                  const isSelected = square.id === selectedSquare;
                  const isLegalDestination = legalDestinations.has(square.id);
                  const isCaptureDestination = captureDestinations.has(square.id);
                  const isLastMove = lastMoveSquares.has(square.id);
                  const isMovingPiece = pieceAnimation?.to === square.id;
                  const pieceAnimationStyle: PieceAnimationStyle | undefined = isMovingPiece
                    ? ({
                        "--move-x": pieceAnimation.deltaX,
                        "--move-y": pieceAnimation.deltaY,
                      } as PieceAnimationStyle)
                    : undefined;

                  return (
                    <button
                      aria-label={square.piece ? `${square.id}, ${square.piece.name}` : `${square.id}, empty`}
                      className={[
                        styles.square,
                        square.isLight ? styles.lightSquare : styles.darkSquare,
                        isSelected ? styles.selectedSquare : "",
                        isLegalDestination ? styles.legalSquare : "",
                        isCaptureDestination ? styles.captureSquare : "",
                        isLastMove ? styles.lastMoveSquare : "",
                      ].join(" ")}
                      disabled={isBusy || !isGameActive}
                      key={square.id}
                      onClick={() => handleSquareClick(square)}
                      type="button"
                    >
                      <span className={styles.coordinate}>{square.id}</span>
                      {square.piece ? (
                        <span
                          className={[styles.pieceMover, isMovingPiece ? styles.movingPiece : ""].join(" ")}
                          key={isMovingPiece ? pieceAnimation.key : `${square.id}-${square.piece.symbol}`}
                          onAnimationEnd={isMovingPiece ? () => clearPieceAnimation(pieceAnimation.key) : undefined}
                          style={pieceAnimationStyle}
                        >
                          <img alt={square.piece.name} draggable={false} src={square.piece.image} />
                        </span>
                      ) : null}
                    </button>
                  );
                })}
              </div>
              {gameResult ? (
                <div className={styles.resultOverlay} aria-live="assertive">
                  <div className={styles.resultPanel} aria-label={`${gameResult.title} ${gameResult.subtitle}`} role="status">
                    <p>{gameResult.title}</p>
                    <span>{gameResult.subtitle}</span>
                  </div>
                </div>
              ) : null}
            </div>
          ) : (
            <div className={styles.loadingBoard}>Loading board</div>
          )}
        </div>

        <aside className={styles.sidePanel}>
          <div className={styles.controlGroup}>
            <label htmlFor="difficulty">Bot level</label>
            <select
              disabled={isBusy}
              id="difficulty"
              onChange={(event) => setDifficulty(event.target.value as Difficulty)}
              value={difficulty}
            >
              {difficulties.map((level) => (
                <option key={level} value={level}>
                  {level}
                </option>
              ))}
            </select>
          </div>

          <label className={styles.toggle}>
            <input checked={autoBot} disabled={isBusy} onChange={(event) => setAutoBot(event.target.checked)} type="checkbox" />
            <span>Auto bot reply</span>
          </label>

          <form className={styles.moveForm} onSubmit={handleMoveSubmit}>
            <label htmlFor="move">UCI move</label>
            <div>
              <input
                disabled={isBusy || !isGameActive}
                id="move"
                maxLength={5}
                onChange={(event) => setMoveDraft(event.target.value)}
                placeholder="e2e4"
                value={moveDraft}
              />
              <button disabled={isBusy || !moveDraft.trim() || !isGameActive} type="submit">
                Move
              </button>
            </div>
          </form>

          <div className={styles.actionGrid}>
            <button disabled={isBusy || !isGameActive} onClick={() => void runBotMove()} type="button">
              Bot move
            </button>
            <button disabled={isBusy || !game?.last_move} onClick={() => void handleUndo()} type="button">
              Undo
            </button>
            <button disabled={isBusy} onClick={() => void handleReset()} type="button">
              Reset
            </button>
            <button disabled={isBusy} onClick={() => void loadGame()} type="button">
              Refresh
            </button>
          </div>

          <dl className={styles.details}>
            <div>
              <dt>Legal moves</dt>
              <dd>{game?.legal_moves.length ?? 0}</dd>
            </div>
            <div>
              <dt>Selected</dt>
              <dd>{selectedSquare ?? "None"}</dd>
            </div>
            <div>
              <dt>API</dt>
              <dd>{pendingAction === "load" ? "Connecting" : error ? "Needs attention" : "Ready"}</dd>
            </div>
          </dl>
        </aside>
      </section>
    </main>
  );
}
