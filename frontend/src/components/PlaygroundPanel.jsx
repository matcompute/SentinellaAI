import { useState } from "react";

const initialForm = {
  use_case: "Review response reliability check",
  prompt: "Draft a warm but concise reply to a 3-star restaurant review without promising anything unsupported.",
  providers: ["gemini", "mock"],
  system_instruction: "Provide a concise, high-quality answer with safe, practical wording.",
};

export function PlaygroundPanel({ onCompare, results, loading }) {
  const [form, setForm] = useState(initialForm);

  const toggleProvider = (provider) => {
    setForm((current) => ({
      ...current,
      providers: current.providers.includes(provider)
        ? current.providers.filter((item) => item !== provider)
        : [...current.providers, provider],
    }));
  };

  return (
    <section className="view-stack">
      <div className="two-column-band">
        <form
          className="surface dense-surface"
          onSubmit={(event) => {
            event.preventDefault();
            onCompare(form);
          }}
        >
          <div className="surface-header">
            <h3>Compare playground</h3>
            <span>Live provider calls</span>
          </div>

          <label>
            Use case
            <input
              value={form.use_case}
              onChange={(event) => setForm({ ...form, use_case: event.target.value })}
            />
          </label>

          <label>
            Prompt
            <textarea
              value={form.prompt}
              onChange={(event) => setForm({ ...form, prompt: event.target.value })}
            />
          </label>

          <label>
            System instruction
            <textarea
              value={form.system_instruction}
              onChange={(event) => setForm({ ...form, system_instruction: event.target.value })}
            />
          </label>

          <div className="channel-pills">
            {["gemini", "mock"].map((provider) => (
              <button
                type="button"
                key={provider}
                className={form.providers.includes(provider) ? "pill active" : "pill"}
                onClick={() => toggleProvider(provider)}
              >
                {provider}
              </button>
            ))}
          </div>

          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? "Comparing..." : "Run comparison"}
          </button>
        </form>

        <section className="surface">
          <div className="surface-header">
            <h3>Provider outputs</h3>
            <span>{results.length} results</span>
          </div>
          <div className="trace-list">
            {results.map((result) => (
              <article className="trace-card" key={`${result.provider}-${result.model}`}>
                <div className="trace-head">
                  <div>
                    <strong>{result.provider}</strong>
                    <small>{result.model} • {result.latency_ms} ms</small>
                  </div>
                  <span className={`status-pill status-${result.status.toLowerCase()}`}>{result.status}</span>
                </div>
                <p>{result.output}</p>
                <small>{result.note}</small>
              </article>
            ))}
          </div>
        </section>
      </div>
    </section>
  );
}

