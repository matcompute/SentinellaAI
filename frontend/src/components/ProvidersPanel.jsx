export function ProvidersPanel({ providers }) {
  return (
    <section className="view-stack">
      <section className="surface">
        <div className="surface-header">
          <h3>Provider registry</h3>
          <span>{providers.length} providers</span>
        </div>
        <div className="provider-grid">
          {providers.map((provider) => (
            <article className="provider-card" key={provider.id}>
              <div className="provider-head">
                <strong>{provider.name}</strong>
                <span className={`status-pill status-${provider.status.toLowerCase()}`}>{provider.status}</span>
              </div>
              <small>{provider.mode}</small>
              <div className="provider-stats">
                <span>Latency: {provider.avg_latency_ms} ms</span>
                <span>Success: {Math.round(provider.success_rate * 100)}%</span>
                <span>Cost: {provider.est_cost_per_1k}</span>
              </div>
              <p>{provider.note}</p>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}

