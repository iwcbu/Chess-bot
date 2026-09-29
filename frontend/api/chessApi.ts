// frontend/api/chessApi.ts

export type GameTurn = "white" | "black";
export type Difficulty = "easy" | "medium" | "hard" | "expert";



export interface GameStatus {
  fen: string;
  turn: GameTurn;
  legal_moves: string[];
  status: string;
  last_move: string | null;
  opening: string | null;
}

export interface NewGameResponse {
  game_id: string;
  state: GameStatus;
}

interface UndoMoveResponse {
  undone_move: string;
  state: GameStatus;
}

const DEFAULT_API_BASE_URL = "";

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

export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
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

export async function newGame() {
  console.log("hello")
  const req = await request<NewGameResponse>(`/api/v1/new-game`, {
    method: "POST"
  })
  const game_id = req.game_id
  localStorage.setItem("gameId", game_id)

  return req
}

export async function getGame(game_id: string) {
  return request<GameStatus>(`/api/v1/game/${game_id}`, { method: "GET" });
}



export async function makeMove( game_id: string, move: string) {
  return request<GameStatus>(`/api/v1/game/${game_id}/move`, {
    method: "POST",
    body: JSON.stringify({ move }),
  });
}

export async function makeBotMove(game_id: string, difficulty: Difficulty, opening: string) {
  return request<GameStatus>(`/api/v1/game/${game_id}/bot-move`, {
    method: "POST",
    body: JSON.stringify({ difficulty, opening }),
  });
}

export async function undoMove(game_id: string) {
  const response = await request<GameStatus | UndoMoveResponse | null>("/api/v1/game/undo", {
    method: "POST",
  });

  if (response && typeof response === "object" && "state" in response) {
    return response.state;
  }

  return response ?? getGame(game_id);
}

export async function resetGame(game_id: string) {
  return request<GameStatus>(`/api/v1/game/${game_id}/reset`, {
    method: "POST",
  });
}

export async function checkHealth() {
  return request<{ status: string }>("/health");
}
