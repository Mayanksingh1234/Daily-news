"use client";

import { memo, useEffect, useState } from "react";
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
  const [briefings, setBriefings] = useState<Briefing[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch briefings
  const fetchBriefings = async () => {
    setLoading(true);
    setError("");

    try {
      const data = await apiRequest("/briefings");

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
  };

  useEffect(() => {
    fetchBriefings();
  }, [refreshKey]);

  // Activate / deactivate briefing
  const toggleActive = async (
    id: string,
    active: boolean
  ) => {
    try {
      const updatedBriefing = await apiRequest(
        `/briefings/${id}`,
        {
          method: "PATCH",
          body: JSON.stringify({
            active: !active,
          }),
        }
      );

      // Update only the changed briefing
      setBriefings((prev) =>
        prev.map((briefing) =>
          briefing.id === id
            ? updatedBriefing
            : briefing
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

  // Delete briefing
  const deleteBriefing = async (id: string) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this briefing?"
    );

    if (!confirmed) return;

    try {
      await apiRequest(`/briefings/${id}`, {
        method: "DELETE",
      });

      // Remove only the deleted briefing
      setBriefings((prev) =>
        prev.filter(
          (briefing) => briefing.id !== id
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
      <section className="mt-8 rounded-xl border border-gray-200 bg-white p-6">
        <p className="text-sm text-gray-500">
          Loading briefings...
        </p>
      </section>
    );
  }

  return (
    <section className="mt-8">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-gray-900">
          Your briefings
        </h2>

        <p className="mt-1 text-sm text-gray-500">
          Manage your scheduled research podcasts.
        </p>
      </div>

      {/* Error */}
      {error && (
        <div className="mb-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600">
          {error}
        </div>
      )}

      {briefings.length === 0 ? (
        <div className="rounded-xl border border-dashed border-gray-300 bg-white p-8 text-center">
          <p className="text-sm text-gray-500">
            You haven't created any briefings yet.
          </p>
        </div>
      ) : (
        <div className="grid gap-4">
          {briefings.map((briefing) => (
            <div
              key={briefing.id}
              className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm"
            >
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="min-w-0">
                  <h3 className="font-medium text-gray-900">
                    {briefing.topic}
                  </h3>

                  <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-sm text-gray-500">
                    <span>
                      Daily at{" "}
                      {briefing.scheduled_time.slice(
                        0,
                        5
                      )}
                    </span>

                    <span>
                      {briefing.timezone}
                    </span>
                  </div>
                </div>

                <div className="flex flex-wrap items-center gap-2">
                  <button
                    onClick={() =>
                      toggleActive(
                        briefing.id,
                        briefing.active
                      )
                    }
                    className={`rounded-lg px-3 py-2 text-xs font-medium ${
                      briefing.active
                        ? "bg-green-100 text-green-700"
                        : "bg-gray-100 text-gray-600"
                    }`}
                  >
                    {briefing.active
                      ? "Active"
                      : "Paused"}
                  </button>

                  <button
                    onClick={() =>
                      deleteBriefing(briefing.id)
                    }
                    className="rounded-lg border border-red-200 px-3 py-2 text-xs font-medium text-red-600 transition hover:bg-red-50"
                  >
                    Delete
                  </button>
                </div>
              </div>
              <EpisodeList briefingId={briefing.id} />
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default memo(BriefingList);