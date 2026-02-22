"""Modern chat UI styles with 3-pane layout support and thinking trace"""

CHAT_UI_STYLES = """
/* === CSS Custom Properties === */
:root {
  --chat-bg: #f8fafc;
  --chat-surface: #ffffff;
  --chat-border: #e2e8f0;
  --chat-text: #1e293b;
  --chat-text-muted: #64748b;
  --chat-primary: #3b82f6;
  --chat-primary-hover: #2563eb;
  --chat-user-bg: #3b82f6;
  --chat-user-text: #ffffff;
  --chat-assistant-bg: #f1f5f9;
  --chat-assistant-text: #1e293b;
  --chat-padding: 1rem;
  --chat-gap: 0.75rem;
  --chat-message-padding: 0.75rem 1rem;
  --chat-border-radius: 0.75rem;
  --chat-message-radius: 1.125rem;
  --chat-font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --chat-font-size: 0.875rem;
  --chat-line-height: 1.5;
  --chat-transition: all 0.2s ease;
  --chat-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  --chat-shadow-lg: 0 4px 12px rgba(0, 0, 0, 0.15);
  --settings-width: 280px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --chat-bg: #0f172a;
    --chat-surface: #1e293b;
    --chat-border: #334155;
    --chat-text: #f1f5f9;
    --chat-text-muted: #94a3b8;
    --chat-assistant-bg: #334155;
    --chat-assistant-text: #f1f5f9;
  }
}

/* === Base Reset === */
*, *::before, *::after { box-sizing: border-box; }
body { margin: 0; font-family: var(--chat-font-family); background: var(--chat-bg); color: var(--chat-text); }

/* === 3-Pane Layout === */
.agui-app {
  display: grid;
  grid-template-columns: var(--settings-width) 1fr;
  height: 100vh;
  overflow: hidden;
}

.agui-settings {
  background: var(--chat-surface);
  border-right: 1px solid var(--chat-border);
  padding: 1.25rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.agui-settings h2 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  color: var(--chat-text);
}

.agui-settings label {
  display: block;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--chat-text-muted);
  margin-bottom: 0.35rem;
}

.agui-settings select,
.agui-settings input[type="text"],
.agui-settings input[type="number"],
.agui-settings textarea {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--chat-border);
  border-radius: 0.5rem;
  background: var(--chat-bg);
  color: var(--chat-text);
  font-size: 0.85rem;
  font-family: var(--chat-font-family);
}

.agui-settings select:focus,
.agui-settings input:focus,
.agui-settings textarea:focus {
  outline: none;
  border-color: var(--chat-primary);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
}

.agui-settings .setting-group {
  display: flex;
  flex-direction: column;
}

.agui-settings .setting-divider {
  border: 0;
  border-top: 1px solid var(--chat-border);
  margin: 0.25rem 0;
}

.agui-main {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* === Header Bar === */
.agui-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
  background: var(--chat-surface);
  border-bottom: 1px solid var(--chat-border);
  min-height: 3rem;
}

.agui-header-title {
  font-size: 0.95rem;
  font-weight: 600;
}

.agui-header-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.agui-think-btn {
  padding: 0.4rem 0.8rem;
  background: transparent;
  border: 1px solid var(--chat-border);
  border-radius: 0.5rem;
  color: var(--chat-text-muted);
  font-size: 0.8rem;
  cursor: pointer;
  transition: var(--chat-transition);
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.agui-think-btn:hover {
  background: var(--chat-bg);
  color: var(--chat-primary);
  border-color: var(--chat-primary);
}

.agui-think-btn.active {
  background: var(--chat-primary);
  color: white;
  border-color: var(--chat-primary);
}

.agui-think-badge {
  background: var(--chat-primary);
  color: white;
  border-radius: 50%;
  width: 1.2rem;
  height: 1.2rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  font-weight: 600;
}

/* === Chat Container === */
.chat-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
  background: var(--chat-bg);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: var(--chat-padding);
  display: flex;
  flex-direction: column;
  gap: var(--chat-gap);
}

.chat-messages:empty::before {
  content: "Start a conversation...";
  color: var(--chat-text-muted);
  text-align: center;
  padding: 3rem;
  font-style: italic;
  font-size: 0.95rem;
}

/* === Message Styles === */
.chat-message {
  display: flex;
  flex-direction: column;
  max-width: 80%;
  animation: chat-message-in 0.3s ease-out;
}

.chat-message-content {
  padding: var(--chat-message-padding);
  border-radius: var(--chat-message-radius);
  font-size: var(--chat-font-size);
  line-height: var(--chat-line-height);
  word-wrap: break-word;
}

.chat-message-content p { margin: 0 0 0.5rem 0; }
.chat-message-content p:last-child { margin-bottom: 0; }
.chat-message-content ul, .chat-message-content ol { margin: 0.5rem 0; padding-left: 1.5rem; }
.chat-message-content li { margin: 0.25rem 0; }

.chat-message-content code {
  background: rgba(0, 0, 0, 0.08);
  padding: 0.125rem 0.3rem;
  border-radius: 0.25rem;
  font-size: 0.85em;
  font-family: 'Courier New', monospace;
}

.chat-message-content pre {
  background: #1e293b;
  color: #e2e8f0;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin: 0.75rem 0;
  font-size: 0.85rem;
  line-height: 1.5;
}

.chat-message-content pre code { background: none; padding: 0; color: inherit; }

.chat-message-content blockquote {
  border-left: 3px solid var(--chat-border);
  padding-left: 1rem;
  margin: 0.5rem 0;
  color: var(--chat-text-muted);
}

.chat-message-content h1, .chat-message-content h2, .chat-message-content h3 {
  margin: 0.75rem 0 0.5rem 0;
  font-weight: 600;
}
.chat-message-content h1 { font-size: 1.25rem; }
.chat-message-content h2 { font-size: 1.1rem; }
.chat-message-content h3 { font-size: 1rem; }

.chat-message-content table { border-collapse: collapse; width: 100%; margin: 0.5rem 0; }
.chat-message-content th, .chat-message-content td { border: 1px solid var(--chat-border); padding: 0.5rem; text-align: left; }
.chat-message-content th { background: rgba(0, 0, 0, 0.05); font-weight: 600; }

@keyframes chat-message-in {
  from { opacity: 0; transform: translateY(0.5rem); }
  to { opacity: 1; transform: translateY(0); }
}

.chat-user { align-self: flex-end; }
.chat-assistant { align-self: flex-start; }

.chat-user .chat-message-content {
  background: var(--chat-user-bg);
  color: var(--chat-user-text);
  border-bottom-right-radius: 0.375rem;
}

.chat-assistant .chat-message-content {
  background: var(--chat-assistant-bg);
  color: var(--chat-assistant-text);
  border-bottom-left-radius: 0.375rem;
}

/* Streaming indicator */
.chat-streaming::after {
  content: '\\25CA';
  animation: chat-blink 1s infinite;
  opacity: 0.7;
  margin-left: 2px;
}

@keyframes chat-blink {
  0%, 50% { opacity: 0.7; }
  51%, 100% { opacity: 0; }
}

/* === Input Form === */
.chat-input {
  padding: var(--chat-padding);
  background: var(--chat-surface);
  border-top: 1px solid var(--chat-border);
}

.chat-status {
  min-height: 1.25rem;
  padding: 0.35rem 0;
  color: var(--chat-text-muted);
  font-size: 0.8rem;
  text-align: center;
}

/* Suggestion Buttons */
#suggestion-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.5rem 0;
}

.suggestion-btn {
  padding: 0.4rem 0.9rem;
  background: var(--chat-surface);
  border: 1px solid var(--chat-border);
  border-radius: 1rem;
  color: var(--chat-primary);
  font-size: 0.8rem;
  font-family: var(--chat-font-family);
  cursor: pointer;
  transition: var(--chat-transition);
  white-space: nowrap;
}

.suggestion-btn:hover {
  background: var(--chat-primary);
  color: white;
  transform: translateY(-1px);
  box-shadow: var(--chat-shadow-lg);
}

.chat-input-form {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.5rem;
  align-items: end;
}

.chat-input-field {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--chat-border);
  border-radius: var(--chat-border-radius);
  background: var(--chat-bg);
  color: var(--chat-text);
  font-family: var(--chat-font-family);
  font-size: 0.95rem;
  line-height: 1.5;
  resize: none;
  min-height: 3rem;
  max-height: 10rem;
  overflow-y: hidden;
  transition: var(--chat-transition);
}

.chat-input-field:focus {
  outline: none;
  border-color: var(--chat-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.chat-input-button {
  padding: 0.65rem 1.25rem;
  background: var(--chat-primary);
  color: white;
  border: none;
  border-radius: var(--chat-border-radius);
  font-family: var(--chat-font-family);
  font-size: var(--chat-font-size);
  font-weight: 500;
  cursor: pointer;
  transition: var(--chat-transition);
  min-height: 3rem;
}

.chat-input-button:hover {
  background: var(--chat-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--chat-shadow-lg);
}

/* === Thinking Trace Panel === */
.agui-thinking-overlay {
  position: fixed;
  top: 0;
  right: -420px;
  width: 400px;
  height: 100vh;
  background: var(--chat-surface);
  border-left: 1px solid var(--chat-border);
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.12);
  z-index: 100;
  display: flex;
  flex-direction: column;
  transition: right 0.3s ease;
}

.agui-thinking-overlay.open {
  right: 0;
}

.agui-thinking-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--chat-border);
  background: var(--chat-surface);
}

.agui-thinking-header h3 {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.agui-thinking-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: var(--chat-text-muted);
  padding: 0.25rem;
  border-radius: 0.25rem;
  line-height: 1;
}

.agui-thinking-close:hover {
  background: var(--chat-bg);
  color: var(--chat-text);
}

.agui-thinking-content {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 1.25rem;
  font-size: 0.825rem;
  line-height: 1.6;
}

.thinking-step {
  padding: 0.75rem;
  margin-bottom: 0.75rem;
  background: var(--chat-bg);
  border-radius: 0.5rem;
  border-left: 3px solid var(--chat-primary);
}

.thinking-step-header {
  font-weight: 600;
  font-size: 0.75rem;
  color: var(--chat-primary);
  margin-bottom: 0.35rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.thinking-step-body {
  color: var(--chat-text);
  white-space: pre-wrap;
  word-break: break-word;
}

.thinking-step.tool-call {
  border-left-color: #f59e0b;
}

.thinking-step.tool-call .thinking-step-header {
  color: #f59e0b;
}

.thinking-step.reasoning {
  border-left-color: #8b5cf6;
}

.thinking-step.reasoning .thinking-step-header {
  color: #8b5cf6;
}

.thinking-streaming::after {
  content: '...';
  animation: thinking-dots 1.4s infinite;
}

@keyframes thinking-dots {
  0%, 20% { content: '.'; }
  40% { content: '..'; }
  60%, 100% { content: '...'; }
}

/* === Tool Messages === */
.chat-tool {
  align-self: center;
  max-width: 60%;
}

.chat-tool .chat-message-content {
  background: var(--chat-border);
  color: var(--chat-text-muted);
  font-size: 0.8rem;
  text-align: center;
  border-radius: var(--chat-border-radius);
  padding: 0.4rem 0.8rem;
}

/* === State Sidebar === */
.chat-state-container {
  background: var(--chat-surface);
  border: 1px solid var(--chat-border);
  border-radius: var(--chat-border-radius);
  padding: var(--chat-padding);
  height: fit-content;
}

/* === Layout Utilities === */
.chat-layout {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: var(--chat-padding);
  height: 100vh;
  padding: var(--chat-padding);
  background: var(--chat-bg);
}

.chat-layout-sidebar { overflow-y: auto; }
.chat-layout-main { display: flex; flex-direction: column; }

/* === Pydantic UI Components (dynamically generated) === */
.pydantic-ui-card {
  background: var(--chat-surface);
  border: 1px solid var(--chat-border);
  border-radius: 0.75rem;
  padding: 1rem;
  margin: 0.5rem 0;
}

.pydantic-ui-card h4 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--chat-primary);
}

.pydantic-ui-field {
  display: flex;
  justify-content: space-between;
  padding: 0.3rem 0;
  border-bottom: 1px solid var(--chat-border);
  font-size: 0.825rem;
}

.pydantic-ui-field:last-child { border-bottom: none; }

.pydantic-ui-field-key {
  color: var(--chat-text-muted);
  font-weight: 500;
}

.pydantic-ui-field-value {
  color: var(--chat-text);
}

/* === Error States === */
.chat-error { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.chat-error .chat-message-content { background: #fef2f2; color: #dc2626; }

/* === Responsive === */
@media (max-width: 768px) {
  .agui-app { grid-template-columns: 1fr; }
  .agui-settings { display: none; }
  .chat-message { max-width: 95%; }
  .agui-thinking-overlay { width: 100%; right: -100%; }
}
"""


def get_chat_styles():
    from fasthtml.common import Style
    return Style(CHAT_UI_STYLES)


def get_custom_theme(**theme_vars):
    from fasthtml.common import Style
    css_vars = []
    for key, value in theme_vars.items():
        css_var = f"--{key.replace('_', '-')}: {value};"
        css_vars.append(css_var)
    return Style(f":root {{ {' '.join(css_vars)} }}")
