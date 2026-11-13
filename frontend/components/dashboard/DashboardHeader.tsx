import { memo } from "react";

interface DashboardHeaderProps {
  userEmail?: string;
}

 function DashboardHeader({
  userEmail,
}: DashboardHeaderProps) {
  return (
    <div className="mb-8">
      <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
        Dashboard
      </h1>

      <p className="mt-2 text-sm text-gray-600 sm:text-base">
        Welcome back{userEmail ? `, ${userEmail}` : ""}.
      </p>

      <p className="mt-1 text-sm text-gray-500">
        Create and manage your scheduled research podcasts.
      </p>
    </div>
  );
}
export default memo(DashboardHeader);