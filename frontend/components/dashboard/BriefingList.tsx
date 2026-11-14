"use client";

import {
  memo,
  useCallback,
  useEffect,
  useState,
} from "react";

import { apiRequest } from "@/lib/api";

import EpisodeList from "./EpisodeList";

interface Briefing {
  id: string;
  topic: string;
  scheduled_time: string;
  timezone: string;
  active: boolean;
  created_at: string;
}

interface BriefingListProps {
  refreshKey: number;
}

function BriefingList({
  refreshKey,
}: BriefingListProps) {
  const [briefings, setBriefings] =
    useState<Briefing[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const fetchBriefings = useCallback(
    async () => {
      try {
        setLoading(true);
        setError("");

        const data = await apiRequest(
          "/briefings"
        );

        setBriefings(data || []);
      } catch (error) {
        setError(
          error instanceof Error
            ? error.message
            : "Failed to load briefings."
        );
      } finally {
        setLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    fetchBriefings();
  }, [fetchBriefings, refreshKey]);

  const handleToggle = async (
    briefing: Briefing
  ) => {
    try {
      await apiRequest(
        `/briefings/${briefing.id}`,
        {
          method: "PATCH",

          body: JSON.stringify({
            active: !briefing.active,
          }),
        }
      );

      setBriefings((previous) =>
        previous.map((item) =>
          item.id === briefing.id
            ? {
                ...item,
                active: !item.active,
              }
            : item
        )
      );
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to update briefing."
      );
    }
  };

  const handleDelete = async (
    briefingId: string
  ) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this briefing?"
    );

    if (!confirmed) {
      return;
    }

    try {
      await apiRequest(
        `/briefings/${briefingId}`,
        {
          method: "DELETE",
        }
      );

      setBriefings((previous) =>
        previous.filter(
          (item) => item.id !== briefingId
        )
      );
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to delete briefing."
      );
    }
  };

  if (loading) {
    return (
      <div className="rounded-xl border bg-white p-6">
        <p className="text-sm text-gray-500">
          Loading briefings...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border border-red-200 bg-red-50 p-6">
        <p className="text-sm text-red-600">
          {error}
        </p>
      </div>
    );
  }

  if (briefings.length === 0) {
    return (
      <div className="rounded-xl border bg-white p-8 text-center">
        <h3 className="text-lg font-semibold text-gray-900">
          No briefings yet
        </h3>

        <p className="mt-2 text-sm text-gray-500">
          Create your first daily research briefing
          above.
        </p>
      </div>
    );
  }

  return (
    <section className="space-y-4">

      <h3 className="text-xl font-semibold text-gray-900">
        Your Briefings
      </h3>

      {briefings.map((briefing) => (
        <div
          key={briefing.id}
          className="rounded-xl border bg-white p-6 shadow-sm"
        >

          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">

            <div>
              <h4 className="text-lg font-semibold text-gray-900">
                {briefing.topic}
              </h4>

              <p className="mt-2 text-sm text-gray-500">
                Every day at{" "}
                <span className="font-medium text-gray-700">
                  {briefing.scheduled_time.slice(
                    0,
                    5
                  )}
                </span>{" "}
                ({briefing.timezone})
              </p>

              <p className="mt-1 text-xs text-gray-400">
                Status:{" "}
                {briefing.active
                  ? "Active"
                  : "Paused"}
              </p>
            </div>

            <div className="flex gap-2">

              <button
                onClick={() =>
                  handleToggle(briefing)
                }
                className="rounded-md border border-gray-300 px-3 py-2 text-xs font-medium text-gray-700 hover:bg-gray-100"
              >
                {briefing.active
                  ? "Pause"
                  : "Activate"}
              </button>

              <button
                onClick={() =>
                  handleDelete(briefing.id)
                }
                className="rounded-md border border-red-200 px-3 py-2 text-xs font-medium text-red-600 hover:bg-red-50"
              >
                Delete
              </button>

            </div>

          </div>

          <EpisodeList
            briefingId={briefing.id}
          />

        </div>
      ))}

    </section>
  );
}

export default memo(BriefingList);