import { useEffect, useState } from "react";
import { EvaluationsPanel } from "./components/EvaluationsPanel";
import { LoginView } from "./components/LoginView";
import { OverviewPanel } from "./components/OverviewPanel";
import { PlaygroundPanel } from "./components/PlaygroundPanel";
import { ProvidersPanel } from "./components/ProvidersPanel";
import { TracesPanel } from "./components/TracesPanel";

const tokenKey = "sentinella_token";
const defaultLogin = { email: "lead@sentinella.io", password: "" };
const navigation = [
  { id: "overview", label: "Overview" },
  { id: "providers", label: "Providers" },
  { id: "traces", label: "Traces" },
  { id: "evaluations", label: "Evaluations" },
  { id: "playground", label: "Playground" },
];

async function apiRequest(path, options = {}, token) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed." }));
    throw new Error(error.detail || "Request failed.");
  }

  return response.json();
}

export default function App() {
  const [token, setToken] = useState(() => window.localStorage.getItem(tokenKey) || "");
  const [user, setUser] = useState(null);
  const [dashboard, setDashboard] = useState({ metrics: [], highlights: [], watch_items: [] });
  const [providers, setProviders] = useState([]);
  const [traces, setTraces] = useState([]);
  const [evaluations, setEvaluations] = useState([]);
  const [rules, setRules] = useState([]);
  const [results, setResults] = useState([]);
  const [loginForm, setLoginForm] = useState(defaultLogin);
  const [activeView, setActiveView] = useState("overview");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function loadWorkspace(currentToken) {
    const [me, loadedDashboard, loadedProviders, loadedTraces, loadedEvaluations, loadedRules] =
      await Promise.all([
        apiRequest("/api/auth/me", {}, currentToken),
        apiRequest("/api/dashboard", {}, currentToken),
        apiRequest("/api/providers", {}, currentToken),
        apiRequest("/api/traces", {}, currentToken),
        apiRequest("/api/evaluations", {}, currentToken),
        apiRequest("/api/routing-rules", {}, currentToken),
      ]);

    setUser(me);
    setDashboard(loadedDashboard);
    setProviders(loadedProviders);
    setTraces(loadedTraces);
    setEvaluations(loadedEvaluations);
    setRules(loadedRules);
  }

  useEffect(() => {
    if (!token) {
      return;
    }

    let cancelled = false;
    setBusy(true);
    setError("");

    loadWorkspace(token)
      .catch((loadError) => {
        if (!cancelled) {
          setToken("");
          window.localStorage.removeItem(tokenKey);
          setError(loadError.message);
        }
      })
      .finally(() => {
        if (!cancelled) {
          setBusy(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [token]);

  const handleLogin = async (event) => {
    event.preventDefault();
    setBusy(true);
    setError("");

    try {
      const result = await apiRequest("/api/auth/login", {
        method: "POST",
        body: JSON.stringify(loginForm),
      });
      setToken(result.access_token);
      window.localStorage.setItem(tokenKey, result.access_token);
    } catch (loginError) {
      setError(loginError.message);
    } finally {
      setBusy(false);
    }
  };

  const handleCompare = async (payload) => {
    setBusy(true);
    setError("");

    try {
      const comparison = await apiRequest(
        "/api/playground/compare",
        {
          method: "POST",
          body: JSON.stringify(payload),
        },
        token,
      );
      setResults(comparison.results);
      setTraces(await apiRequest("/api/traces", {}, token));
      setActiveView("playground");
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  };

  if (!token) {
    return (
      <LoginView
        form={loginForm}
        setForm={setLoginForm}
        onSubmit={handleLogin}
        error={error}
        loading={busy}
      />
    );
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-lockup">
          <span className="eyebrow">AI Ops</span>
          <h1>Sentinella</h1>
          <p>{user?.role}</p>
        </div>

        <nav className="nav-list">
          {navigation.map((item) => (
            <button
              key={item.id}
              type="button"
              className={activeView === item.id ? "nav-item active" : "nav-item"}
              onClick={() => setActiveView(item.id)}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      <main className="workspace">
        <header className="workspace-header">
          <div>
            <span className="eyebrow">Reliability workspace</span>
            <h2>{navigation.find((item) => item.id === activeView)?.label}</h2>
          </div>
          <div className="workspace-badges">
            <span>Provider visibility</span>
            <span>Trace review</span>
            <span>Fallback rules</span>
          </div>
        </header>

        {error ? <p className="error-banner inline">{error}</p> : null}

        {activeView === "overview" ? <OverviewPanel dashboard={dashboard} /> : null}
        {activeView === "providers" ? <ProvidersPanel providers={providers} /> : null}
        {activeView === "traces" ? <TracesPanel traces={traces} /> : null}
        {activeView === "evaluations" ? <EvaluationsPanel evaluations={evaluations} rules={rules} /> : null}
        {activeView === "playground" ? (
          <PlaygroundPanel onCompare={handleCompare} results={results} loading={busy} />
        ) : null}
      </main>
    </div>
  );
}
