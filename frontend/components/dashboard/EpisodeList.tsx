"use client";

import { memo, useEffect, useState } from "react";
import { apiRequest } from "@/lib/api";

interface Episode {
  id: string;
  briefing_id: string;
  title: string;
  script?: string;
  audio_url?: string;
  status: string;
  error_message?: string;
  generated_at?: string;
  created_at: string;
}

interface EpisodeListProps {
  briefingId: string;
}

function EpisodeList({
  briefingId,
}: EpisodeListProps) {
  const [episodes, setEpisodes] = useState<Episode[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchEpisodes = async () => {
      try {
        setLoading(true);
        setError("");

        const data = await apiRequest(
          `/briefings/${briefingId}/episodes`
        );

        setEpisodes(data || []);
      } catch (error) {
        setError(
          error instanceof Error
            ? error.message
            : "Failed to load episodes."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchEpisodes();
  }, [briefingId]);

  if (loading) {
    return (
      <div className="mt-4 rounded-lg bg-gray-50 p-4">
        <p className="text-sm text-gray-500">
          Loading episodes...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mt-4 rounded-lg bg-red-50 p-4">
        <p className="text-sm text-red-600">
          {error}
        </p>
      </div>
    );
  }

  if (episodes.length === 0) {
    return (
      <div className="mt-4 rounded-lg border border-dashed border-gray-300 p-4">
        <p className="text-sm text-gray-500">
          No episodes generated yet.
        </p>
      </div>
    );
  }

  return (
    <div className="mt-4 space-y-3">
      {episodes.map((episode) => (
        <div
          key={episode.id}
          className="rounded-lg border border-gray-200 bg-gray-50 p-4"
        >
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div className="min-w-0">
              <h4 className="font-medium text-gray-900">
                {episode.title}
              </h4>

              <p className="mt-1 text-xs text-gray-500">
                {new Date(
                  episode.created_at
                ).toLocaleString("en-IN")}
              </p>
            </div>

            <span
              className={`w-fit rounded-full px-2.5 py-1 text-xs font-medium ${
                episode.status === "ready"
                  ? "bg-green-100 text-green-700"
                  : episode.status === "failed"
                  ? "bg-red-100 text-red-700"
                  : "bg-yellow-100 text-yellow-700"
              }`}
            >
              {episode.status}
            </span>
          </div>

          {episode.status === "ready" &&
            episode.audio_url && (
              <div className="mt-4">
                <audio
                  controls
                  preload="metadata"
                  className="w-full"
                  src={episode.audio_url}
                />
              </div>
            )}

          {episode.status !== "ready" &&
            episode.status !== "failed" && (
              <p className="mt-3 text-sm text-gray-500">
                Your podcast is being generated...
              </p>
            )}

          {episode.status === "failed" &&
            episode.error_message && (
              <p className="mt-3 text-sm text-red-600">
                {episode.error_message}
              </p>
            )}

          {episode.status === "ready" &&
            episode.script && (
              <details className="mt-4">
                <summary className="cursor-pointer text-sm font-medium text-gray-700">
                  View transcript
                </summary>

                <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-gray-600">
                  {episode.script}
                </p>
              </details>
            )}
        </div>
      ))}
    </div>
  );
}

export default memo(EpisodeList);