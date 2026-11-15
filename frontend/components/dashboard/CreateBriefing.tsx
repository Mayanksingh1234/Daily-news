"use client";

import {
  FormEvent,
  memo,
  useState,
} from "react";

import { apiRequest } from "@/lib/api";

interface CreateBriefingProps {
  onCreated: () => void;
}

function CreateBriefing({
  onCreated,
}: CreateBriefingProps) {
  const [topic, setTopic] = useState("");

  const [hour, setHour] = useState("08");
  const [minute, setMinute] = useState("00");
  const [period, setPeriod] = useState("AM");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (
    event: FormEvent
  ) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (!topic.trim()) {
      setError("Please enter a research topic.");
      return;
    }

    // Convert 12-hour time to 24-hour time
    let hour24 = Number(hour);

    if (period === "AM") {
      if (hour24 === 12) {
        hour24 = 0;
      }
    } else {
      if (hour24 !== 12) {
        hour24 += 12;
      }
    }

    const scheduledTime = `${String(hour24).padStart(
      2,
      "0"
    )}:${minute}:00`;

    try {
      setLoading(true);

      await apiRequest("/briefings", {
        method: "POST",

        body: JSON.stringify({
          topic: topic.trim(),
          scheduled_time: scheduledTime,
          timezone: "Asia/Kolkata",
        }),
      });

      setTopic("");
      setHour("08");
      setMinute("00");
      setPeriod("AM");

      setSuccess(
        "Briefing created successfully."
      );

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
    <section className="mb-8 rounded-xl border bg-white p-6 shadow-sm">
      <div className="mb-5">
        <h3 className="text-lg font-semibold text-gray-900">
          Create Daily Briefing
        </h3>

        <p className="mt-1 text-sm text-gray-500">
          Choose a topic and the time you want your
          daily podcast generated.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="space-y-4"
      >
        {/* Research Topic */}

        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">
            Research Topic
          </label>

          <input
            type="text"
            value={topic}
            onChange={(event) =>
              setTopic(event.target.value)
            }
            placeholder="e.g. Startup funding announced in the last 24 hours"
            className="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none focus:border-gray-900"
          />
        </div>

        {/* Daily Time */}

        <div>
          <label className="mb-2 block text-sm font-medium text-gray-700">
            Daily Time
          </label>

          <div className="flex items-center gap-2">

            {/* Hour */}

            <select
              value={hour}
              onChange={(event) =>
                setHour(event.target.value)
              }
              className="rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 outline-none focus:border-gray-900"
            >
              {Array.from(
                { length: 12 },
                (_, index) => {
                  const value = String(
                    index + 1
                  ).padStart(2, "0");

                  return (
                    <option
                      key={value}
                      value={value}
                    >
                      {value}
                    </option>
                  );
                }
              )}
            </select>

            <span className="text-lg font-medium">
              :
            </span>

            {/* Minute */}

           <select
              value={minute}
              onChange={(event) =>
                setMinute(event.target.value)
              }
              className="rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 outline-none focus:border-gray-900"
            >
              {Array.from(
                { length: 60 },
                (_, index) => {
                  const value = String(
                    index
                  ).padStart(2, "0");

                  return (
                    <option
                      key={value}
                      value={value}
                    >
                      {value}
                    </option>
                  );
                }
              )}
            </select>

            {/* AM / PM */}

           <select
              value={period}
              onChange={(event) =>
                setPeriod(event.target.value)
              }
              className="rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 outline-none focus:border-gray-900"
            >
              <option value="AM">
                AM
              </option>

              <option value="PM">
                PM
              </option>
            </select>

          </div>
        </div>

        {/* Messages */}

        {error && (
          <p className="text-sm text-red-600">
            {error}
          </p>
        )}

        {success && (
          <p className="text-sm text-green-600">
            {success}
          </p>
        )}

        {/* Submit */}

        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-gray-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading
            ? "Creating..."
            : "Create Briefing"}
        </button>
      </form>
    </section>
  );
}

export default memo(CreateBriefing);