const greetingElement = document.querySelector("#greeting");
const retryButton = document.querySelector("#retry");

function setState(state, message) {
  greetingElement.className = `status status--${state}`;
  greetingElement.replaceChildren();

  if (state === "loading") {
    const spinner = document.createElement("span");
    spinner.className = "spinner";
    spinner.setAttribute("aria-hidden", "true");
    greetingElement.append(spinner);
  }

  const text = document.createElement("span");
  text.textContent = message;
  greetingElement.append(text);
  retryButton.hidden = state !== "error";
}

async function loadGreeting() {
  setState("loading", "Loading greeting…");

  try {
    const response = await fetch("/api/greeting", {
      headers: { Accept: "application/json" },
    });

    if (!response.ok) {
      throw new Error(`Greeting request failed with status ${response.status}`);
    }

    const data = await response.json();
    if (typeof data.greeting !== "string" || data.greeting.length === 0) {
      throw new Error("Greeting response was invalid");
    }

    setState("success", data.greeting);
  } catch (error) {
    console.error(error);
    setState("error", "The greeting could not be loaded.");
  }
}

retryButton.addEventListener("click", loadGreeting);
loadGreeting();

