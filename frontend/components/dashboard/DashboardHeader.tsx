"use client";

import { memo } from "react";

interface DashboardHeaderProps {
  userEmail?: string;
}

function DashboardHeader({
  userEmail,
}: DashboardHeaderProps) {
  return (
    <div className="mb-8">
      <h2 className="text-lg sm:text-xl md:text-2xl font-bold text-gray-900">
        Your Daily Briefings
      </h2>

      <p className="mt-2 text-gray-600">
        Create research topics and receive AI-generated
        podcast episodes every day.
      </p>
    </div>
  );
}

export default memo(DashboardHeader);