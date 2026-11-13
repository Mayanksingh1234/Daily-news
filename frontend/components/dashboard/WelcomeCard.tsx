export default function WelcomeCard() {
  return (
    <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-gray-900">
        Your briefings
      </h2>

      <p className="mt-2 text-sm text-gray-600">
        Your scheduled research briefings and generated podcast episodes
        will appear here.
      </p>

      <button
        className="mt-5 rounded-lg bg-black px-4 py-2 text-sm font-medium text-white transition hover:bg-gray-800"
      >
        Create briefing
      </button>
    </section>
  );
}