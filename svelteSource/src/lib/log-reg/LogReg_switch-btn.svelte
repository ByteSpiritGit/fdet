<script lang="ts">
   export let selectedButton = "register";
   const theOther = selectedButton === "register" ? "login" : "register";

   function handleMouseLeave(buttonId) {
      if (buttonId === selectedButton) {
         selectedButton = buttonId === "register" ? "login" : "register";
      }
   }
</script>

<section class="switch-button">
   <a
      class="register-btn {selectedButton === 'register' ? 'selected' : 'notSelected'}"
      on:mouseenter={() => (selectedButton = "register")}
      on:mouseleave={() => handleMouseLeave(theOther)}
      href="/users/register">Register</a
   >
   <a
      class="login-btn {selectedButton === 'login' ? 'selected' : 'notSelected'}"
      on:mouseenter={() => (selectedButton = "login")}
      on:mouseleave={() => handleMouseLeave(theOther)}
      href="/users/login">Login</a
   >
</section>

<style>
   .switch-button {
      display: flex;
      flex-direction: row;
      justify-content: space-evenly;
      align-items: center;

      padding: 0;
      margin: 0;
   }

   .switch-button > a {
      width: 100%;

      border: none;

      padding: 0.4em;

      text-decoration: none;
      color: var(--color-text);

      text-align: center;
      font-size: 1em;

      transition: 0.1s;
   }

   .switch-button > a:focus {
      border: none;
      outline: 2px solid var(--color-text);
      outline-offset: -2px;
   }

   .register-btn {
      border-radius: 0.3em 0 0 0.3em;
   }

   .login-btn {
      border-radius: 0 0.3em 0.3em 0;
   }

   .selected {
      background-color: var(--color-tertiary);
   }

   .notSelected {
      background-color: var(--color-primary-alpha);
   }
</style>