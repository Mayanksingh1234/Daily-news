"use client";

import { memo, FormEvent, useState } from "react";
import { apiRequest } from "@/lib/api";

interface CreateBriefingProps {
  onCreated: () => void;
}

function CreateBriefing({
  onCreated,
}: CreateBriefingProps) {
  const [topic, setTopic] = useState("");
  const [time, setTime] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (
    e: FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    if (!topic.trim() || !time) {
      setError(
        "Please enter a topic and select a time."
      );
      return;
    }

    setLoading(true);

    try {
      await apiRequest("/briefings", {
        method: "POST",
        body: JSON.stringify({
          topic: topic.trim(),
          scheduled_time: `${time}:00`,
          timezone: "Asia/Kolkata",
        }),
      });

      setTopic("");
      setTime("");
      setSuccess("Briefing created successfully.");

      onCreated();
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to create briefing."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-gray-900">
          Create a briefing
        </h2>

        <p className="mt-1 text-sm text-gray-500">
          Choose a research topic and the time you want
          your daily podcast.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="space-y-5"
      >
        {/* Topic */}
        <div>
          <label
            htmlFor="topic"
            className="mb-2 block text-sm font-medium text-gray-700"
          >
            Research topic
          </label>

          <input
            id="topic"
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g. Startup funding announced in the last 24 hours"
            className="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm outline-none transition focus:border-black focus:ring-1 focus:ring-black"
          />
        </div>

        {/* Time */}
        <div>
          <label
            htmlFor="time"
            className="mb-2 block text-sm font-medium text-gray-700"
          >
            Daily delivery time
          </label>

          <input
            id="time"
            type="time"
            value={time}
            onChange={(e) => setTime(e.target.value)}
            className="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm outline-none transition focus:border-black focus:ring-1 focus:ring-black sm:max-w-xs"
          />
        </div>

        {/* Error */}
        {error && (
          <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600">
            {error}
          </div>
        )}

        {/* Success */}
        {success && (
          <div className="rounded-lg bg-green-50 px-4 py-3 text-sm text-green-600">
            {success}
          </div>
        )}

        {/* Submit */}
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-black px-5 py-3 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Creating..." : "Create briefing"}
        </button>
      </form>
    </section>
  );
}

export default memo(CreateBriefing);