export function OverviewPanel({ dashboard }) {
  return (
    <section className="view-stack">
      <div className="hero-band">
        <div>
          <span className="eyebrow">Control tower</span>
          <h2>Know which provider is healthy, fast, and safe before users notice drift.</h2>
        </div>
        <p>
          Sentinella keeps traces, evaluations, routing policy, and provider health visible in one
          engineering workspace.
        </p>
      </div>

      <div className="metric-grid">
        {dashboard.metrics.map((metric) => (
          <article className="metric-panel" key={metric.label}>
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
            <small>{metric.detail}</small>
            <em>{metric.trend}</em>
          </article>
        ))}
      </div>

      <div className="two-column-band">
        <section className="surface">
          <div className="surface-header">
            <h3>Watch items</h3>
            <span>Today</span>
          </div>
          <ul className="bullet-list">
            {dashboard.watch_items.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>

        <section className="surface">
          <div className="surface-header">
            <h3>Recent highlights</h3>
            <span>AI ops</span>
          </div>
          <div className="timeline">
            {dashboard.highlights.map((item) => (
              <article className={`timeline-item tone-${item.tone}`} key={item.id}>
                <strong>{item.title}</strong>
                <p>{item.detail}</p>
              </article>
            ))}
          </div>
        </section>
      </div>
    </section>
  );
}

