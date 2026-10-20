// SkillX Main JS

// Auto-dismiss alerts
document.addEventListener('DOMContentLoaded', function() {
  const alerts = document.querySelectorAll('.skillx-alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      alert.style.transition = '0.3s ease';
      setTimeout(() => alert.remove(), 300);
    }, 4000);
  });

  // Animate score bars
  document.querySelectorAll('.score-bar-fill').forEach(bar => {
    const width = bar.getAttribute('data-width') || bar.style.width;
    bar.style.width = '0';
    requestAnimationFrame(() => {
      setTimeout(() => { bar.style.width = width; }, 100);
    });
  });

  // Animate XP bars
  document.querySelectorAll('.xp-bar-fill').forEach(bar => {
    const width = bar.getAttribute('data-width') || bar.style.width;
    bar.style.width = '0';
    requestAnimationFrame(() => {
      setTimeout(() => { bar.style.width = width; }, 200);
    });
  });

  // Skill chip selection
  initSkillChips();

  // Auto-scroll chat to bottom
  const chatMessages = document.querySelector('.chat-messages');
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});

function initSkillChips() {
  const chips = document.querySelectorAll('[data-skill-chip]');
  chips.forEach(chip => {
    chip.addEventListener('click', function() {
      const mode = document.querySelector('.setup-tab.active')?.getAttribute('data-mode') || 'have';
      const skillId = this.getAttribute('data-skill-id');
      const haveInput = document.getElementById(`have_${skillId}`);
      const wantInput = document.getElementById(`want_${skillId}`);

      if (mode === 'have') {
        if (this.classList.contains('selected-have')) {
          this.classList.remove('selected-have');
          if (haveInput) haveInput.disabled = true;
        } else {
          this.classList.add('selected-have');
          this.classList.remove('selected-want');
          if (haveInput) haveInput.disabled = false;
          if (wantInput) wantInput.disabled = true;
        }
      } else {
        if (this.classList.contains('selected-want')) {
          this.classList.remove('selected-want');
          if (wantInput) wantInput.disabled = true;
        } else {
          this.classList.add('selected-want');
          this.classList.remove('selected-have');
          if (wantInput) wantInput.disabled = false;
          if (haveInput) haveInput.disabled = true;
        }
      }
    });
  });
}

function switchTab(tab, mode) {
  document.querySelectorAll('.setup-tab').forEach(t => t.classList.remove('active'));
  tab.classList.add('active');
  tab.setAttribute('data-mode', mode);
  document.querySelectorAll('.setup-tab').forEach(t => {
    if (t !== tab) t.removeAttribute('data-mode');
  });
}

// Test timer
function startTimer(seconds, elementId) {
  let remaining = seconds;
  const el = document.getElementById(elementId);
  if (!el) return;
  const interval = setInterval(() => {
    remaining--;
    const m = Math.floor(remaining / 60);
    const s = remaining % 60;
    el.textContent = `${m}:${s.toString().padStart(2, '0')}`;
    if (remaining <= 60) el.style.color = '#f87171';
    if (remaining <= 0) {
      clearInterval(interval);
      document.getElementById('test-form')?.submit();
    }
  }, 1000);
}

// Video controls
function toggleMic() {
  const btn = document.getElementById('micBtn');
  btn?.classList.toggle('muted');
  btn.innerHTML = btn.classList.contains('muted')
    ? '<i class="fas fa-microphone-slash"></i>'
    : '<i class="fas fa-microphone"></i>';
}

function toggleCam() {
  const btn = document.getElementById('camBtn');
  btn?.classList.toggle('muted');
  btn.innerHTML = btn.classList.contains('muted')
    ? '<i class="fas fa-video-slash"></i>'
    : '<i class="fas fa-video"></i>';
}

function endCall() {
  if (confirm('End this session?')) {
    window.history.back();
  }
}
