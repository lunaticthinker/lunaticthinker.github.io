---
title: "Contact"
date: 2025-11-17
draft: false
---

## Get in Touch

Have a question, suggestion, or just want to say hello? Feel free to reach out using the form below. Your message will create a GitHub issue in our repository, allowing for transparent communication and tracking.

<form action="https://github.com/lunaticthinker-me/lunaticthinker.github.io/issues/new" method="get" id="contact-form" class="contact-form">
  <div class="form-group">
    <label for="issue-title">Subject *</label>
    <input type="text" id="issue-title" name="title" required placeholder="Brief description of your message" minlength="10" maxlength="100">
  </div>
  
  <div class="form-group">
    <label for="issue-body">Message *</label>
    <textarea id="issue-body" name="body" required placeholder="Your message here..." rows="8" minlength="20"></textarea>
  </div>
  
  <div class="form-group">
    <label for="issue-labels">Topic</label>
    <select id="issue-labels" name="labels">
      <option value="question">Question</option>
      <option value="feedback">Feedback</option>
      <option value="collaboration">Collaboration</option>
      <option value="bug">Bug Report</option>
      <option value="other">Other</option>
    </select>
  </div>
  
  <div class="form-group honeypot" style="display: none;">
    <label for="website">Website</label>
    <input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
  </div>
  
  <button type="submit" class="submit-btn">Send Message</button>
  
  <p class="form-note">
    <small>* Required fields. Submitting this form will redirect you to GitHub where you can review and submit your message as an issue. You'll need a GitHub account to complete the submission.</small>
  </p>
</form>

<style>
.contact-form {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: var(--card-background);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--text-color);
}

.form-group input[type="text"],
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  background: var(--input-background);
  color: var(--text-color);
  transition: border-color 0.3s;
}

.form-group input[type="text"]:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--link-color);
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: var(--link-color);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.submit-btn:hover {
  opacity: 0.9;
}

.form-note {
  margin-top: 1rem;
  color: var(--text-color-secondary);
  text-align: center;
}

.honeypot {
  position: absolute;
  left: -9999px;
}

@media (max-width: 768px) {
  .contact-form {
    padding: 1rem;
  }
}
</style>

<script>
document.getElementById('contact-form').addEventListener('submit', function(e) {
  // Check honeypot field (spam protection)
  const honeypot = document.getElementById('website');
  if (honeypot.value !== '') {
    e.preventDefault();
    alert('Spam detected. Form submission blocked.');
    return false;
  }
  
  // Format the issue body with metadata
  const bodyTextarea = document.getElementById('issue-body');
  const originalBody = bodyTextarea.value;
  const timestamp = new Date().toISOString();
  const userAgent = navigator.userAgent;
  
  // Add metadata to help identify legitimate submissions
  const formattedBody = `${originalBody}

---

**Metadata (for spam prevention)**
- Submitted: ${timestamp}
- User Agent: ${userAgent}
- Form Version: 1.0`;
  
  bodyTextarea.value = formattedBody;
});
</script>

---

### Alternative Contact Methods

You can also find me on:

- **GitHub**: [@lunaticthinker](https://github.com/lunaticthinker)  [@dragoscirjan](https://github.com/dragoscirjan)
- **Direct Issues**: [Create an issue directly on GitHub](https://github.com/lunaticthinker-me/lunaticthinker.github.io/issues/new)

### Privacy Note

All messages submitted through this form are public and will be visible in the GitHub repository's issues section. Please do not include sensitive personal information.
