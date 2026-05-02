export function TracesPanel({ traces }) {
  return (
    <section className="view-stack">
      <section className="surface">
        <div className="surface-header">
          <h3>Trace explorer</h3>
          <span>{traces.length} traces</span>
        </div>
        <div className="trace-list">
          {traces.map((trace) => (
            <article className="trace-card" key={trace.id}>
              <div className="trace-head">
                <div>
                  <strong>{trace.use_case}</strong>
                  <small>
                    {trace.provider} • {trace.model} • {trace.latency_ms} ms
                  </small>
                </div>
                <span className={`status-pill status-${trace.status.toLowerCase()}`}>{trace.status}</span>
              </div>
              <p><strong>Prompt:</strong> {trace.prompt_excerpt}</p>
              <p><strong>Output:</strong> {trace.output_excerpt}</p>
              <small>Risk: {trace.risk_level}</small>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}

