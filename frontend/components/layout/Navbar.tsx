"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase/client";

interface NavbarProps {
  userEmail?: string;
}

export default function Navbar({ userEmail }: NavbarProps) {
  const router = useRouter();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    router.push("/login");
  };

  return (
    <nav className="border-b border-gray-200 bg-white">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">

        {/* Logo */}
        <button
          onClick={() => router.push("/")}
          className="flex items-center gap-2"
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-black text-sm font-bold text-white cursor-pointer">
            SP
          </div>

          <span className="text-lg font-semibold text-gray-900">
            Scheduled Podcast
          </span>
        </button>

        {/* Desktop Navigation */}
        <div className="hidden items-center gap-6 md:flex">
          <button
            onClick={() => router.push("/")}
            className="text-sm font-medium text-gray-700 transition hover:text-black"
          >
            Dashboard
          </button>

          <span className="max-w-[220px] truncate text-sm text-gray-500">
            {userEmail}
          </span>

          <button
            onClick={handleLogout}
            className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-100"
          >
            Logout
          </button>
        </div>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="rounded-lg border border-gray-300 px-3 py-2 text-sm md:hidden"
        >
          Menu
        </button>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="border-t border-gray-200 bg-white px-4 py-4 md:hidden">
          <div className="flex flex-col gap-3">
            <button
              onClick={() => {
                router.push("/");
                setMenuOpen(false);
              }}
              className="rounded-lg px-3 py-2 text-left text-sm font-medium text-gray-700 hover:bg-gray-100"
            >
              Dashboard
            </button>

            <div className="px-3 py-2 text-sm text-gray-500">
              {userEmail}
            </div>

            <button
              onClick={handleLogout}
              className="rounded-lg border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700"
            >
              Logout
            </button>
          </div>
        </div>
      )}
    </nav>
  );
}