export function EvaluationsPanel({ evaluations, rules }) {
  return (
    <section className="view-stack">
      <div className="two-column-band">
        <section className="surface">
          <div className="surface-header">
            <h3>Evaluations</h3>
            <span>{evaluations.length} runs</span>
          </div>
          <div className="evaluation-list">
            {evaluations.map((item) => (
              <article className="evaluation-card" key={item.id}>
                <strong>{item.use_case}</strong>
                <p>{item.baseline_provider} vs {item.challenger_provider}</p>
                <small>{item.verdict}</small>
                <div className="delta-grid">
                  <span>Quality {item.quality_delta}</span>
                  <span>Cost {item.cost_delta}</span>
                  <span>Latency {item.latency_delta}</span>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="surface">
          <div className="surface-header">
            <h3>Routing rules</h3>
            <span>{rules.length} rules</span>
          </div>
          <div className="rule-list">
            {rules.map((rule) => (
              <article className="rule-card" key={rule.id}>
                <strong>{rule.name}</strong>
                <small>Priority {rule.priority} • {rule.status}</small>
                <p>{rule.condition}</p>
                <em>{rule.action}</em>
              </article>
            ))}
          </div>
        </section>
      </div>
    </section>
  );
}

