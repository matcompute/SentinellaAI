export function LoginView({ form, setForm, onSubmit, error, loading }) {
  return (
    <div className="login-shell">
      <div className="login-copy">
        <span className="eyebrow">AI Reliability Platform</span>
        <h1>Sentinella</h1>
        <p>
          Provider visibility, trace review, evaluations, and routing control for teams that ship LLM
          systems in the real world.
        </p>
      </div>

      <form className="login-panel" onSubmit={onSubmit}>
        <div className="panel-header">
          <span className="eyebrow">Engineering Access</span>
          <h2>Sign in</h2>
        </div>

        <label>
          Email
          <input
            type="email"
            value={form.email}
            onChange={(event) => setForm({ ...form, email: event.target.value })}
            placeholder="operator@sentinella.local"
          />
        </label>

        <label>
          Password
          <input
            type="password"
            value={form.password}
            onChange={(event) => setForm({ ...form, password: event.target.value })}
            placeholder="Configured in backend .env"
          />
        </label>

        {error ? <p className="error-banner">{error}</p> : null}

        <button className="primary-button" type="submit" disabled={loading}>
          {loading ? "Signing in..." : "Enter control tower"}
        </button>
      </form>
    </div>
  );
}
