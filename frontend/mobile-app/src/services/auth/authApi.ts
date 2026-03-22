export type LoginRequest = {
  email: string;
  password: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

const API_BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export const loginWithEmailPassword = async (
  payload: LoginRequest,
): Promise<LoginResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Login failed. Check your credentials and backend availability.");
  }

  const body = (await response.json()) as LoginResponse;

  if (!body.access_token) {
    throw new Error("Login response did not include an access token.");
  }

  return body;
};
