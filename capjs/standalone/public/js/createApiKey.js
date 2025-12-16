import { createModal } from "./utils.js";
import { openSettings } from "./settings.js";
import sendApiRequest from "./api.js";

async function openCreateApiKey() {
  const modal = createModal(
    "Add a key",
    `<div class="content">
      <label for="key-name">Key name</label>
      <input type="text" name="key-name" class="key-name-input" max-length="200" required>
     </div>

     <button class="create-key-button primary" disabled>Create API key</button>`
  );
  modal.querySelector(".key-name-input").focus();

  const focus = [
    {sel: ".key-name-input", focus: true},
    {sel: ".create-key-button", focus: false},
    {sel: ".close-button", focus: false},
  ];
  modal
  .addEventListener("keydown", (event) => {
    if (event.key === "Tab") {
      event.preventDefault();
      const curr = focus.findIndex((v) => v.focus);
      const tabnext = (p, inc) => {
        let n = (((p + inc) % focus.length) + focus.length) % focus.length;
        while (p != n && modal.querySelector(focus[n].sel).disabled) {
          n = (((n + inc) % focus.length) + focus.length) % focus.length;
        }
        return n;
      };
      if (event.shiftKey) {
        focus[curr].focus = false;
        let n = tabnext(curr, -1);
        console.log(`change focus to from ${curr} to ${n}`)
        focus[n].focus = true;
        modal.querySelector(focus[n].sel).focus();
      }
      else {
        focus[curr].focus = false;
        let n = tabnext(curr, 1)
        console.log(`change focus to from ${curr} to ${n}`)
        focus[n].focus = true;
        modal.querySelector(focus[n].sel).focus();
      }
    }
  });

  modal.querySelector(".key-name-input").addEventListener("input", (event) => {
    modal.querySelector(".create-key-button").disabled =
      !event.target.value.trim();
  });

  modal
    .querySelector(".key-name-input")
    .addEventListener("keydown", (event) => {
      if (event.target.value.trim() && event.key === "Enter") {
        modal.querySelector(".create-key-button").click();
      }
    });

  modal.querySelector(".close-button").addEventListener("click", () => {
    document.body.removeChild(modal);
  });

  modal
    .querySelector(".create-key-button")
    .addEventListener("click", async () => {
      const name = modal.querySelector(".key-name-input").value.trim();

      modal.querySelector(".create-key-button").disabled = true;

      try {
        const { apiKey } = await sendApiRequest("POST", "/settings/apikeys", {
          name,
        });

        document.body.removeChild(modal);

        const successModal = createModal(
          "Key created",
          `<div class="content">
            <label for="api-key">API key</label>
            <input type="text" name="api-key" value="${apiKey}" readonly>

            <p class="small-text">Make sure to copy your API key as it will not be shown again later.</p>
          </div>

          <button class="close-small-button primary secondary">Close</button>`
        );

        successModal
          .querySelector(".close-small-button")
          .addEventListener("click", () => {
            document.body.removeChild(successModal);
          });

        openSettings();
      } catch (error) {
        createModal(
          "Error",
          `<div class="content"><p>Failed to create API key: ${error.message}</p></div>`
        );
        modal.querySelector(".create-key-button").disabled = false;
      }
    });
}

document
  .querySelector(".create-api-key")
  .addEventListener("click", openCreateApiKey);

export default openCreateApiKey;
