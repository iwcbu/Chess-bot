// frontend/api/chessApi.ts

export type GameTurn = "white" | "black";
export type Difficulty = "easy" | "medium" | "hard" | "expert";

export interface GameStatus {
  fen: string;
  turn: GameTurn;
  legal_moves: string[];
  status: string;
  last_move: string | null;
  bot_opening: string | null;
}

interface UndoMoveResponse {
  undone_move: string;
  state: GameStatus;
}

const DEFAULT_API_BASE_URL = "http://localhost:8000";

const getApiBaseUrl = () => {
  const configuredUrl = import.meta.env.VITE_CHESS_API_URL as string | undefined;
  return (configuredUrl || DEFAULT_API_BASE_URL).replace(/\/+$/, "");
};

const getErrorMessage = (body: unknown, fallback: string) => {
  if (body && typeof body === "object" && "detail" in body) {
    const detail = (body as { detail?: unknown }).detail;
    if (typeof detail === "string") {
      return detail;
    }
  }

  return fallback;
};

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  const text = await response.text();
  const body = text ? (JSON.parse(text) as unknown) : null;

  if (!response.ok) {
    throw new Error(getErrorMessage(body, `Request failed with ${response.status}`));
  }

  return body as T;
}

export async function getGame() {
  return request<GameStatus>("/game", { method: "GET" });
}

export async function makeMove(move: string) {
  return request<GameStatus>("/api/v1/game/move", {
    method: "POST",
    body: JSON.stringify({ move }),
  });
}

export async function makeBotMove(difficulty: Difficulty, opening: string | null) {

  return request<GameStatus>("/api/v1/game/bot-move", {
    method: "POST",
    body: JSON.stringify({ difficulty, opening }),

  });
}

export async function undoMove() {
  const response = await request<GameStatus | UndoMoveResponse | null>("/api/v1/game/undo", {
    method: "POST",
  });

  if (response && typeof response === "object" && "state" in response) {
    return response.state;
  }

  return response ?? getGame();
}

export async function resetGame() {
  return request<GameStatus>("/api/v1/game/reset", {
    method: "POST",
  });
}

export async function checkHealth() {
  return request<{ status: string }>("/health");
}
