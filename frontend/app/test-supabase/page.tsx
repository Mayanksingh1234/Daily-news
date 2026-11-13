"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase/client";

export default function TestSupabasePage() {
  const [status, setStatus] = useState("Testing connection...");

  useEffect(() => {
    const testConnection = async () => {
      const { error } = await supabase
        .from("profiles")
        .select("id")
        .limit(1);

      if (error) {
        setStatus(`Connection failed: ${error.message}`);
        return;
      }

      setStatus("Supabase connected successfully.");
    };

    testConnection();
  }, []);

  return (
    <main className="flex min-h-screen items-center justify-center">
      <div className="rounded-lg border p-8">
        <h1 className="text-xl font-semibold">
          Supabase Connection
        </h1>

        <p className="mt-3 text-gray-600">
          {status}
        </p>
      </div>
    </main>
  );
}