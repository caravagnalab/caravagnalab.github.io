(() => {
  const dialog = document.querySelector("#join-dialog");
  const form = document.querySelector("#join-enquiry-form");
  const topic = document.querySelector("#join-topic");
  const closeButton = document.querySelector(".join-dialog-close");
  const openButtons = document.querySelectorAll("[data-join-topic]");
  const result = document.querySelector("#join-email-ready");
  const resultCloseButton = document.querySelector(".join-result-close");
  const preview = document.querySelector("#join-email-preview");
  const openEmail = document.querySelector("#join-open-email");
  const copyEmail = document.querySelector("#join-copy-email");
  const copyStatus = document.querySelector("#join-copy-status");
  const editEnquiry = document.querySelector("#join-edit-enquiry");

  if (
    !dialog || !form || !topic || !closeButton || !openButtons.length ||
    !result || !resultCloseButton || !preview || !openEmail ||
    !copyEmail || !copyStatus || !editEnquiry
  ) return;

  let opener = null;
  let preparedMessage = "";

  const openDialog = (button) => {
    opener = button;
    const requestedTopic = button.dataset.joinTopic || "";
    topic.value = [...topic.options].some((option) => option.value === requestedTopic)
      ? requestedTopic
      : "";
    form.hidden = false;
    result.hidden = true;
    copyStatus.textContent = "";
    dialog.showModal();
    window.requestAnimationFrame(() => {
      const firstField = form.querySelector("input[name='first_name']");
      dialog.scrollTop = 0;
      if (firstField) firstField.focus({ preventScroll: true });
    });
  };

  const closeDialog = () => {
    dialog.close();
    if (opener) opener.focus();
  };

  openButtons.forEach((button) => {
    button.addEventListener("click", () => openDialog(button));
  });

  closeButton.addEventListener("click", closeDialog);
  resultCloseButton.addEventListener("click", closeDialog);

  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) closeDialog();
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const data = new FormData(form);
    const firstName = String(data.get("first_name") || "").trim();
    const lastName = String(data.get("last_name") || "").trim();
    const enquiry = String(data.get("topic") || "").trim();
    const cvLink = String(data.get("cv_link") || "").trim();

    const subject = `${enquiry} enquiry — ${firstName} ${lastName}`;
    const body = [
      "Dear Giulio,",
      "",
      `I am writing to enquire about: ${enquiry}.`,
      "",
      `Name: ${firstName} ${lastName}`,
      `Email: ${String(data.get("email") || "").trim()}`,
      `Current position: ${String(data.get("current_position") || "").trim()}`,
      `Institution / employer: ${String(data.get("affiliation") || "").trim()}`,
      `Location: ${String(data.get("location") || "").trim() || "Not specified"}`,
      `CV: ${cvLink || "I will attach my CV to this email."}`,
      "",
      "Motivation:",
      String(data.get("motivation") || "").trim(),
      "",
      "Best wishes,",
      `${firstName} ${lastName}`,
    ].join("\n");

    preparedMessage = `Subject: ${subject}\n\n${body}`;
    preview.value = preparedMessage;
    openEmail.href =
      `mailto:gcaravagna@units.it?subject=${encodeURIComponent(subject)}` +
      `&body=${encodeURIComponent(body)}`;
    form.hidden = true;
    result.hidden = false;
    copyStatus.textContent = "";
    dialog.scrollTop = 0;
    openEmail.focus({ preventScroll: true });
  });

  editEnquiry.addEventListener("click", () => {
    result.hidden = true;
    form.hidden = false;
    copyStatus.textContent = "";
    dialog.scrollTop = 0;
    const firstField = form.querySelector("input[name='first_name']");
    if (firstField) firstField.focus({ preventScroll: true });
  });

  copyEmail.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(preparedMessage);
      copyStatus.textContent = "Message copied to the clipboard.";
    } catch {
      preview.focus();
      preview.select();
      copyStatus.textContent = "Select and copy the message from the preview.";
    }
  });
})();
