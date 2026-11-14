"use client";

import { memo } from "react";
import { useRouter } from "next/navigation";
import { useDispatch } from "react-redux";

import { supabase } from "@/lib/supabase/client";

import type { AppDispatch } from "@/store/store";
import { clearUser } from "@/store/slices/userSlice";

interface NavbarProps {
  userEmail?: string;
}

function Navbar({ userEmail }: NavbarProps) {
  const router = useRouter();
  const dispatch = useDispatch<AppDispatch>();

  const handleLogout = async () => {
    await supabase.auth.signOut();

    dispatch(clearUser());

    router.replace("/login");
  };

  return (
    <nav className="border-b bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">

        {/* Logo / Brand */}
        <div className="min-w-0">
          <h1 className="truncate text-lg font-semibold text-gray-900 sm:text-xl md:text-3xl">
            Daily Podcast Agent
          </h1>

          <p className="hidden text-xs text-gray-500 sm:block">
            AI-powered research briefings
          </p>
        </div>

        {/* User Section */}
        <div className="flex shrink-0 items-center gap-2 sm:gap-4">

          {userEmail && (
            <span className="hidden max-w-[220px] truncate text-sm text-gray-600 md:block">
              {userEmail}
            </span>
          )}

          <button
            onClick={handleLogout}
            className="rounded-md border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-100 sm:px-4"
          >
            Logout
          </button>

        </div>

      </div>
    </nav>
  );
}

export default memo(Navbar);