<!-- Editorial content for join.qmd. -->

::: {.join-page}
<header class="join-heading">
<p class="eyebrow">Join the laboratory</p>
<h1>Work with us.</h1>
<p>We welcome researchers and students who want to develop computational methods around real biological and clinical questions.</p>
</header>

<section class="join-opportunities">
<div class="join-opportunities-heading">
<p class="eyebrow">Ways to join</p>
<h2>Choose the route that fits your stage.</h2>
<p>Opportunities depend on active funding, doctoral calls and available supervision.</p>
</div>

<div class="join-role-grid">
{{< include includes/join-opportunities.html >}}
</div>
</section>

<section class="join-contact">
<p class="eyebrow">Before you write</p>
<h2>Tell us what you want to work on.</h2>
<p>Introduce your background, the questions that interest you and why the laboratory may be a good fit. Include a CV and relevant links.</p>
<button class="join-apply-button" type="button" data-join-topic=""><i class="bi bi-person-plus"></i> Apply to join</button>
</section>

<dialog id="join-dialog" class="join-dialog" aria-labelledby="join-dialog-title">
<form id="join-enquiry-form" class="join-form">
<header class="join-form-header">
<div>
<p class="eyebrow">Enquire about joining</p>
<h2 id="join-dialog-title">Tell us about yourself.</h2>
</div>
<button class="join-dialog-close" type="button" aria-label="Close enquiry form"><i class="bi bi-x-lg"></i></button>
</header>

<div class="join-form-grid">
<label>First name <input name="first_name" autocomplete="given-name" required></label>
<label>Last name <input name="last_name" autocomplete="family-name" required></label>
<label>Email <input name="email" type="email" autocomplete="email" required></label>
<label>Current location <input name="location" autocomplete="country-name" placeholder="City, country"></label>
<label class="join-form-wide">Current institution or employer <input name="affiliation" autocomplete="organization" required></label>
<label>Current position
<select name="current_position" required>
<option value="" selected disabled>Select one</option>
<option>Postdoctoral researcher</option>
<option>PhD researcher</option>
<option>MSc student</option>
<option>BSc student</option>
<option>Research scientist</option>
<option>Other</option>
</select>
</label>
<label>Enquiry
<select id="join-topic" name="topic" required>
<option value="" selected disabled>Select one</option>
<option>Postdoctoral position</option>
<option>Postdoctoral fellowship application</option>
<option>PhD position</option>
<option>MSc or BSc project</option>
<option>Internship or research visit</option>
<option>Other collaboration</option>
</select>
</label>
<label class="join-form-wide">CV link <input name="cv_link" type="url" inputmode="url" placeholder="https://…" aria-describedby="cv-help"></label>
<p id="cv-help" class="join-field-help join-form-wide">Share a Drive, Dropbox, institutional or personal link. If you prefer, leave this blank and attach your CV when your email client opens.</p>
<label class="join-form-wide">Motivation
<textarea name="motivation" rows="7" minlength="80" maxlength="2500" required placeholder="What would you like to work on, and why does the laboratory seem like a good fit?"></textarea>
</label>
</div>

<label class="join-form-confirm">
<input name="email_acknowledgement" type="checkbox" required>
<span>I understand that this form creates an email draft and does not upload or store files.</span>
</label>

<footer class="join-form-footer">
<p><i class="bi bi-shield-check"></i> Your answers remain in this browser until you open the email draft.</p>
<button class="join-form-submit" type="submit"><i class="bi bi-envelope-arrow-up"></i> Prepare email</button>
</footer>
</form>

<section id="join-email-ready" class="join-email-ready" hidden aria-live="polite">
<header class="join-form-header">
<div>
<p class="eyebrow">Email prepared</p>
<h2>Your enquiry is ready.</h2>
</div>
<button class="join-dialog-close join-result-close" type="button" aria-label="Close prepared email"><i class="bi bi-x-lg"></i></button>
</header>
<div class="join-email-ready-body">
<p>The message below is addressed to <strong>gcaravagna@units.it</strong>. Open it in your email application and attach your CV if you did not provide a link.</p>
<label>Message preview
<textarea id="join-email-preview" rows="15" readonly></textarea>
</label>
<p id="join-copy-status" class="join-copy-status" role="status"></p>
</div>
<footer class="join-form-footer join-email-actions">
<button id="join-edit-enquiry" class="join-secondary" type="button"><i class="bi bi-pencil"></i> Edit answers</button>
<button id="join-copy-email" class="join-secondary" type="button"><i class="bi bi-copy"></i> Copy message</button>
<a id="join-open-email" class="join-form-submit" href="#"><i class="bi bi-envelope-arrow-up"></i> Open email app</a>
</footer>
</section>
</dialog>
:::

<script src="assets/join-form.js" defer></script>
