import { supabase } from "@/lib/supabase/client";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

async function getAccessToken() {
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session?.access_token) {
    throw new Error(
      "User is not authenticated"
    );
  }

  return session.access_token;
}

export async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
) {
  const token = await getAccessToken();

  const response = await fetch(
    `${API_URL}${endpoint}`,
    {
      ...options,

      headers: {
        "Content-Type": "application/json",

        Authorization: `Bearer ${token}`,

        ...(options.headers || {}),
      },
    }
  );

  if (!response.ok) {
    const error =
      await response.json().catch(() => ({
        detail: "Request failed",
      }));

    throw new Error(
      error.detail || "Request failed"
    );
  }

  return response.json();
}