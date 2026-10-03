import { FormEvent, useCallback, useEffect, useState } from 'react';

type Task = {
  id: number;
  title: string;
  done: boolean;
  createdAt: string;
};

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:3000';

async function readError(response: Response) {
  const body = await response.json().catch(() => ({}));
  return body.error ?? 'Something went wrong. Please try again.';
}

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const loadTasks = useCallback(async () => {
    setError('');
    try {
      const response = await fetch(`${API_URL}/tasks`);
      if (!response.ok) throw new Error(await readError(response));
      setTasks(await response.json());
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to load tasks.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadTasks();
  }, [loadTasks]);

  async function addTask(event: FormEvent) {
    event.preventDefault();
    const trimmedTitle = title.trim();
    if (!trimmedTitle) return;

    setSaving(true);
    setError('');
    try {
      const response = await fetch(`${API_URL}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: trimmedTitle }),
      });
      if (!response.ok) throw new Error(await readError(response));
      const task: Task = await response.json();
      setTasks((currentTasks) => [task, ...currentTasks]);
      setTitle('');
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to add task.');
    } finally {
      setSaving(false);
    }
  }

  async function toggleTask(task: Task) {
    setError('');
    try {
      const response = await fetch(`${API_URL}/tasks/${task.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ done: !task.done }),
      });
      if (!response.ok) throw new Error(await readError(response));
      const updatedTask: Task = await response.json();
      setTasks((currentTasks) => currentTasks.map((item) => (item.id === updatedTask.id ? updatedTask : item)));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to update task.');
    }
  }

  const completedCount = tasks.filter((task) => task.done).length;

  return (
    <main className="page-shell">
      <section className="task-card" aria-labelledby="page-title">
        <div className="eyebrow">PERSONAL TASK BOARD</div>
        <div className="heading-row">
          <div>
            <h1 id="page-title">Make space for what matters.</h1>
            <p className="subtitle">A simple place to capture today’s next steps.</p>
          </div>
          <div className="progress-badge" aria-label={`${completedCount} of ${tasks.length} tasks completed`}>
            <strong>{completedCount}</strong>
            <span>done</span>
          </div>
        </div>

        <form className="task-form" onSubmit={addTask}>
          <label className="sr-only" htmlFor="task-title">New task</label>
          <input
            id="task-title"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            placeholder="What needs doing?"
            maxLength={120}
          />
          <button type="submit" disabled={saving || !title.trim()}>{saving ? 'Adding…' : 'Add task'}</button>
        </form>

        {error && <p className="error-message" role="alert">{error}</p>}

        <div className="task-list" aria-live="polite">
          {loading ? (
            <p className="empty-state">Loading your tasks…</p>
          ) : tasks.length === 0 ? (
            <p className="empty-state">Your list is clear. Add your first task above.</p>
          ) : (
            tasks.map((task) => (
              <label className={`task-row ${task.done ? 'is-done' : ''}`} key={task.id}>
                <input type="checkbox" checked={task.done} onChange={() => void toggleTask(task)} />
                <span>{task.title}</span>
              </label>
            ))
          )}
        </div>
      </section>
    </main>
  );
}

export default App;
