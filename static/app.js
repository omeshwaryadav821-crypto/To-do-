/**
 * Mochi Tasks - Reliable, Minimalist & Interactive Frontend
 * Focus: Functionality first, clean light blue minimal design, cartoon mascot.
 */

const state = {
  tasks: [],
  filter: 'all',
  creature: { name: 'Mochi', xp: 20, level: 1, progress_pct: 20 },
  pendingBreakdown: null,
  activeReminderId: null
};

// ============================================================================
// 1. WEB AUDIO API CHIMES (NO EXTERNAL FILES)
// ============================================================================
let audioCtx = null;
function getAudioContext() {
  if (!audioCtx) {
    const AudioClass = window.AudioContext || window.webkitAudioContext;
    if (AudioClass) audioCtx = new AudioClass();
  }
  if (audioCtx && audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
  return audioCtx;
}

function playCompleteChime() {
  const ctx = getAudioContext();
  if (!ctx) return;
  const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
  notes.forEach((freq, idx) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const start = ctx.currentTime + idx * 0.07;
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, start);
    gain.gain.setValueAtTime(0.15, start);
    gain.gain.exponentialRampToValueAtTime(0.001, start + 0.3);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(start);
    osc.stop(start + 0.3);
  });
}

function playPetChime() {
  const ctx = getAudioContext();
  if (!ctx) return;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  const now = ctx.currentTime;
  osc.type = 'triangle';
  osc.frequency.setValueAtTime(500, now);
  osc.frequency.exponentialRampToValueAtTime(1000, now + 0.12);
  gain.gain.setValueAtTime(0.18, now);
  gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start(now);
  osc.stop(now + 0.15);
}

function playBellChime() {
  const ctx = getAudioContext();
  if (!ctx) return;
  [880, 1174.66].forEach((freq, idx) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const start = ctx.currentTime + idx * 0.15;
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, start);
    gain.gain.setValueAtTime(0.2, start);
    gain.gain.exponentialRampToValueAtTime(0.001, start + 0.6);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(start);
    osc.stop(start + 0.6);
  });
}

// ============================================================================
// 2. CONFETTI CELEBRATION
// ============================================================================
let confettiParticles = [];
let confettiTimer = null;

function fireConfetti() {
  const canvas = document.getElementById('confetti-canvas');
  if (!canvas) return;
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  const ctx = canvas.getContext('2d');

  const colors = ['#38bdf8', '#bae6fd', '#ff6b6b', '#f59e0b', '#10b981'];
  confettiParticles = [];

  for (let i = 0; i < 50; i++) {
    confettiParticles.push({
      x: window.innerWidth * 0.5 + (Math.random() * 160 - 80),
      y: window.innerHeight * 0.3,
      vx: (Math.random() - 0.5) * 12,
      vy: Math.random() * -10 - 4,
      size: Math.random() * 7 + 4,
      color: colors[Math.floor(Math.random() * colors.length)],
      rotation: Math.random() * 360,
      vRot: (Math.random() - 0.5) * 8,
      opacity: 1
    });
  }

  if (confettiTimer) cancelAnimationFrame(confettiTimer);

  const start = Date.now();
  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const elapsed = Date.now() - start;

    confettiParticles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.4;
      p.rotation += p.vRot;
      p.opacity = Math.max(0, 1 - (elapsed / 1800));

      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate((p.rotation * Math.PI) / 180);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = p.opacity;
      ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
      ctx.restore();
    });

    if (elapsed < 1800) {
      confettiTimer = requestAnimationFrame(render);
    } else {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
  }
  confettiTimer = requestAnimationFrame(render);
}

// ============================================================================
// 3. MASCOT COMPANION (MOCHI)
// ============================================================================
function updateCreatureDisplay(msg = null) {
  const speech = document.getElementById('mochi-speech');
  const level = document.getElementById('mochi-level');
  const xpBar = document.getElementById('mochi-xp-bar');
  const xpText = document.getElementById('mochi-xp-text');

  if (msg && speech) speech.textContent = msg;
  if (level) level.textContent = `Level ${state.creature.level || 1}`;
  if (xpBar) xpBar.style.width = `${state.creature.progress_pct || 0}%`;
  if (xpText) xpText.textContent = `${state.creature.progress_pct || 0}/100 XP`;
}

function celebrateMochi(cheer) {
  const svg = document.getElementById('mochi-svg');
  const eyesNormal = document.getElementById('eyes-normal');
  const eyesHappy = document.getElementById('eyes-happy');

  if (svg) {
    svg.classList.remove('celebrate');
    void svg.offsetWidth;
    svg.classList.add('celebrate');
  }

  if (eyesNormal && eyesHappy) {
    eyesNormal.style.display = 'none';
    eyesHappy.style.display = 'block';
    setTimeout(() => {
      eyesNormal.style.display = 'block';
      eyesHappy.style.display = 'none';
    }, 2000);
  }

  playCompleteChime();
  fireConfetti();
  updateCreatureDisplay(cheer || "Awesome work! 🎉 +20 XP");
}

async function petMochi() {
  playPetChime();
  const svg = document.getElementById('mochi-svg');
  if (svg) {
    svg.classList.remove('celebrate');
    void svg.offsetWidth;
    svg.classList.add('celebrate');
  }

  try {
    const res = await fetch('/api/creature/pet', { method: 'POST' });
    if (res.ok) {
      const data = await res.json();
      state.creature = data.creature;
      updateCreatureDisplay(data.cheer);
    }
  } catch (err) {
    console.error('Error petting Mochi:', err);
  }
}

// ============================================================================
// 4. API & DATA SYNC
// ============================================================================
async function fetchTasks() {
  try {
    const url = state.filter !== 'all' ? `/api/tasks?status=${state.filter}` : '/api/tasks';
    const res = await fetch(url);
    if (res.ok) {
      state.tasks = await res.json();
      renderTasks();
    }
  } catch (err) {
    console.error('Failed to fetch tasks:', err);
  }
}

async function fetchCreature() {
  try {
    const res = await fetch('/api/creature');
    if (res.ok) {
      state.creature = await res.json();
      updateCreatureDisplay();
    }
  } catch (err) {
    console.error('Failed to fetch creature:', err);
  }
}

async function fetchQuickSuggestions() {
  try {
    const res = await fetch('/api/suggestions/quick');
    if (res.ok) {
      const suggestions = await res.json();
      renderSuggestions(suggestions);
    }
  } catch (err) {
    console.error('Failed to fetch suggestions:', err);
  }
}

// ============================================================================
// 5. TASK CREATION (ROCK SOLID & FUNCTIONAL)
// ============================================================================
async function handleTaskSubmit(e) {
  e.preventDefault();

  const input = document.getElementById('task-input');
  const title = input.value.trim();
  if (!title) return;

  const category = document.getElementById('task-category').value;
  const preset = document.getElementById('task-reminder-preset').value;

  // Calculate reminder ISO string if chosen
  let reminder_at = null;
  const now = new Date();

  if (preset === '15m') {
    reminder_at = new Date(now.getTime() + 15 * 60000).toISOString();
  } else if (preset === '1h') {
    reminder_at = new Date(now.getTime() + 60 * 60000).toISOString();
  } else if (preset === 'tomorrow') {
    const tmrw = new Date();
    tmrw.setDate(tmrw.getDate() + 1);
    tmrw.setHours(9, 0, 0, 0);
    reminder_at = tmrw.toISOString();
  } else if (preset === 'custom') {
    const customVal = document.getElementById('task-reminder-custom').value;
    if (customVal) reminder_at = new Date(customVal).toISOString();
  }

  const subtasks = state.pendingBreakdown || [];

  // Reset input immediately for speed
  input.value = '';
  document.getElementById('task-reminder-preset').value = 'none';
  document.getElementById('task-reminder-custom').style.display = 'none';
  clearBreakdown();

  await createTask(title, category, reminder_at, subtasks);
}

async function createTask(title, category = 'General', reminder_at = null, subtasks = []) {
  try {
    const res = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, category, reminder_at, subtasks })
    });

    if (res.ok) {
      const data = await res.json();
      state.tasks.unshift(data.task);
      state.creature = data.creature;
      renderTasks();
      updateCreatureDisplay("Task added! You got this! ✨");
    } else {
      const err = await res.json();
      alert(`Could not add task: ${err.error || 'Server error'}`);
    }
  } catch (err) {
    console.error('Error adding task:', err);
    alert('Failed to connect to server. Ensure python3 server.py is running.');
  }
}

async function toggleTask(taskId) {
  try {
    const res = await fetch(`/api/tasks/${taskId}/toggle`, { method: 'POST' });
    if (res.ok) {
      const data = await res.json();
      state.creature = data.creature;

      // Update in state
      const idx = state.tasks.findIndex(t => t.id === taskId);
      if (idx !== -1) {
        state.tasks[idx] = data.task;
        renderTasks();
      }

      if (data.task.status === 'completed') {
        celebrateMochi(data.cheer);
      } else {
        updateCreatureDisplay("Task unchecked! Take your time 🌱");
      }
    }
  } catch (err) {
    console.error('Error toggling task:', err);
  }
}

async function toggleSubtask(taskId, subtaskId) {
  const task = state.tasks.find(t => t.id === taskId);
  if (!task) return;

  const subtasks = task.subtasks || [];
  const st = subtasks.find(s => s.id === subtaskId);
  if (st) st.completed = !st.completed;

  try {
    const res = await fetch(`/api/tasks/${taskId}/subtasks`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ subtasks })
    });
    if (res.ok) {
      const updated = await res.json();
      const idx = state.tasks.findIndex(t => t.id === taskId);
      if (idx !== -1) {
        state.tasks[idx] = updated;
        renderTasks();
      }
    }
  } catch (err) {
    console.error('Error updating subtask:', err);
  }
}

async function deleteTask(taskId) {
  try {
    const res = await fetch(`/api/tasks/${taskId}`, { method: 'DELETE' });
    if (res.ok) {
      state.tasks = state.tasks.filter(t => t.id !== taskId);
      renderTasks();
      updateCreatureDisplay("Task deleted! 🧹");
    }
  } catch (err) {
    console.error('Error deleting task:', err);
  }
}

// ============================================================================
// 6. SUGGESTIONS & BREAKDOWN
// ============================================================================
async function handleBreakdown() {
  const input = document.getElementById('task-input');
  const title = input.value.trim();

  if (!title) {
    input.focus();
    updateCreatureDisplay("Type a task title first, then click Steps! 🪄");
    return;
  }

  try {
    const res = await fetch('/api/suggestions/breakdown', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title })
    });

    if (res.ok) {
      const data = await res.json();
      state.pendingBreakdown = data.subtasks;

      const box = document.getElementById('breakdown-box');
      const list = document.getElementById('breakdown-list');
      box.style.display = 'block';

      list.innerHTML = data.subtasks.map((s, i) => `
        <li>
          <strong>${i + 1}.</strong> ${escapeHtml(s.text)}
        </li>
      `).join('');

      updateCreatureDisplay("Steps generated! Click 'Add Task' to save them! 🪄");
    }
  } catch (err) {
    console.error('Breakdown error:', err);
  }
}

function clearBreakdown() {
  state.pendingBreakdown = null;
  document.getElementById('breakdown-box').style.display = 'none';
}

function renderSuggestions(suggestions) {
  const container = document.getElementById('suggestions-container');
  if (!container) return;

  container.innerHTML = suggestions.map(s => `
    <button type="button" class="suggestion-chip" data-title="${escapeHtml(s.title)}" data-category="${escapeHtml(s.category)}">
      + ${escapeHtml(s.title)}
    </button>
  `).join('');
}

// ============================================================================
// 7. RENDERING TASKS
// ============================================================================
function renderTasks() {
  const list = document.getElementById('tasks-list');
  const counter = document.getElementById('tasks-counter');
  if (!list) return;

  const total = state.tasks.length;
  const completed = state.tasks.filter(t => t.status === 'completed').length;
  if (counter) counter.textContent = `${completed}/${total} completed`;

  if (state.tasks.length === 0) {
    list.innerHTML = `
      <div class="empty-state">
        <p>No tasks here! Type a task above and press Enter 🚀</p>
      </div>
    `;
    return;
  }

  list.innerHTML = state.tasks.map(task => {
    const isDone = task.status === 'completed';
    const subtasks = task.subtasks || [];
    const doneSubtasks = subtasks.filter(s => s.completed).length;

    let reminderTag = '';
    if (task.reminder_at) {
      const remDate = new Date(task.reminder_at);
      const timeStr = remDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      reminderTag = `<span class="tag tag-reminder">⏰ ${timeStr}</span>`;
    }

    return `
      <div class="task-item ${isDone ? 'completed' : ''}" data-task-id="${task.id}">
        <div class="task-top">
          <div class="task-left">
            <input 
              type="checkbox" 
              class="task-check" 
              data-action="toggle" 
              data-task-id="${task.id}" 
              ${isDone ? 'checked' : ''}
            >
            <span class="task-text">${escapeHtml(task.title)}</span>
          </div>

          <div class="task-badges">
            <span class="tag tag-category">${escapeHtml(task.category)}</span>
            ${reminderTag}
            <button class="btn-icon" data-action="delete" data-task-id="${task.id}" title="Delete">🗑️</button>
          </div>
        </div>

        ${subtasks.length > 0 ? `
          <div class="task-subtasks">
            <span style="font-size: 0.78rem; font-weight: 700; color: var(--blue-600); margin-bottom: 2px;">
              Steps (${doneSubtasks}/${subtasks.length}):
            </span>
            ${subtasks.map(s => `
              <label class="subtask-item">
                <input 
                  type="checkbox" 
                  class="subtask-check" 
                  data-action="subtask-toggle" 
                  data-task-id="${task.id}" 
                  data-subtask-id="${s.id}" 
                  ${s.completed ? 'checked' : ''}
                >
                <span class="subtask-text ${s.completed ? 'checked' : ''}">${escapeHtml(s.text)}</span>
              </label>
            `).join('')}
          </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

// ============================================================================
// 8. REMINDERS POLLER
// ============================================================================
async function checkReminders() {
  try {
    const res = await fetch('/api/reminders/due');
    if (!res.ok) return;
    const dueList = await res.json();

    if (dueList.length > 0) {
      const due = dueList[0];
      if (state.activeReminderId !== due.id) {
        showReminderBanner(due);
      }
    }
  } catch (err) {
    console.error('Error checking reminders:', err);
  }
}

function showReminderBanner(task) {
  state.activeReminderId = task.id;
  playBellChime();

  const banner = document.getElementById('reminder-banner');
  document.getElementById('banner-title').textContent = `Reminder: ${task.title}`;
  document.getElementById('banner-time').textContent = `Category: ${task.category} • Scheduled time is up!`;
  banner.style.display = 'flex';

  updateCreatureDisplay(`Ding! Reminder for: "${task.title}"! ⏰`);

  document.getElementById('btn-banner-done').onclick = async () => {
    await fetch(`/api/tasks/${task.id}/clear-reminder`, { method: 'POST' });
    await toggleTask(task.id);
    banner.style.display = 'none';
    state.activeReminderId = null;
  };

  document.getElementById('btn-banner-snooze').onclick = async () => {
    await fetch(`/api/tasks/${task.id}/snooze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ minutes: 15 })
    });
    banner.style.display = 'none';
    state.activeReminderId = null;
    fetchTasks();
  };

  document.getElementById('btn-banner-close').onclick = async () => {
    await fetch(`/api/tasks/${task.id}/clear-reminder`, { method: 'POST' });
    banner.style.display = 'none';
    state.activeReminderId = null;
    fetchTasks();
  };
}

// ============================================================================
// 9. EVENT LISTENERS
// ============================================================================
function setupEvents() {
  // Task form submission
  document.getElementById('task-form').addEventListener('submit', handleTaskSubmit);

  // Breakdown button
  document.getElementById('btn-breakdown').addEventListener('click', handleBreakdown);
  document.getElementById('btn-clear-breakdown').addEventListener('click', clearBreakdown);

  // Reminder preset toggle custom input
  document.getElementById('task-reminder-preset').addEventListener('change', (e) => {
    const custom = document.getElementById('task-reminder-custom');
    custom.style.display = e.target.value === 'custom' ? 'inline-block' : 'none';
  });

  // Pet Mochi Mascot
  document.getElementById('mochi-pet-target').addEventListener('click', petMochi);

  // Filter buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.filter = btn.dataset.filter;
      fetchTasks();
    });
  });

  // Task list click delegation
  document.getElementById('tasks-list').addEventListener('click', (e) => {
    const target = e.target.closest('[data-action]');
    if (!target) return;

    const action = target.dataset.action;
    const taskId = parseInt(target.dataset.taskId, 10);

    if (action === 'toggle') {
      toggleTask(taskId);
    } else if (action === 'subtask-toggle') {
      const subId = parseInt(target.dataset.subtaskId, 10);
      toggleSubtask(taskId, subId);
    } else if (action === 'delete') {
      deleteTask(taskId);
    }
  });

  // Quick suggestions click delegation
  document.getElementById('suggestions-container').addEventListener('click', (e) => {
    const chip = e.target.closest('.suggestion-chip');
    if (!chip) return;
    const title = chip.dataset.title;
    const category = chip.dataset.category;
    createTask(title, category);
  });
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// ============================================================================
// 10. INITIALIZATION
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
  setupEvents();
  fetchTasks();
  fetchCreature();
  fetchQuickSuggestions();
  setInterval(checkReminders, 15000);
});
