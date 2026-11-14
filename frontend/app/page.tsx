"use client";

import { useCallback, useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useRouter } from "next/navigation";

import { supabase } from "@/lib/supabase/client";

import type { RootState, AppDispatch } from "@/store/store";
import {
  setUser,
  clearUser,
} from "@/store/slices/userSlice";

import Navbar from "@/components/layout/Navbar";
import DashboardHeader from "@/components/dashboard/DashboardHeader";
import CreateBriefing from "@/components/dashboard/CreateBriefing";
import BriefingList from "@/components/dashboard/BriefingList";

export default function HomePage() {
  const router = useRouter();

  const dispatch = useDispatch<AppDispatch>();

  const { user, loading } = useSelector(
    (state: RootState) => state.user
  );

  const [refreshKey, setRefreshKey] = useState(0);

  /*
   * Called after a new briefing is created.
   * This forces BriefingList to fetch the latest data.
   */
  const handleBriefingCreated = useCallback(() => {
    setRefreshKey((previous) => previous + 1);
  }, []);

  /*
   * Check Supabase authentication
   * and put the authenticated user into Redux.
   */
  useEffect(() => {
    const checkUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();

      if (!user) {
        dispatch(clearUser());
        router.replace("/login");
        return;
      }

      dispatch(
        setUser({
          id: user.id,
          email: user.email,
          fullName:
            user.user_metadata?.full_name ||
            user.user_metadata?.name,
        })
      );
    };

    checkUser();

    /*
     * Keep Redux synchronized with Supabase Auth.
     */
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        if (!session?.user) {
          dispatch(clearUser());
          router.replace("/login");
          return;
        }

        dispatch(
          setUser({
            id: session.user.id,
            email: session.user.email,
            fullName:
              session.user.user_metadata?.full_name ||
              session.user.user_metadata?.name,
          })
        );
      }
    );

    return () => {
      subscription.unsubscribe();
    };
  }, [dispatch, router]);

  /*
   * Loading authentication state.
   */
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-sm text-gray-500">
          Loading...
        </p>
      </div>
    );
  }

  /*
   * No authenticated user.
   */
  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar userEmail={user.email} />

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">

        <DashboardHeader
          userEmail={user.email}
        />

        <CreateBriefing
          onCreated={handleBriefingCreated}
        />

        <BriefingList
          refreshKey={refreshKey}
        />

      </main>
    </div>
  );
}