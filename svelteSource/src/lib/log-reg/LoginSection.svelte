<script lang="ts">
   import { onMount } from "svelte";
   import Button from "../Button.svelte";
    import LogRegSwitchBtn from "./LogReg_switch-btn.svelte";

   let user: {
      firstName: string;
      lastName: string;
      email: string;
      username: string;
      password: string;
      confirmPassword: string;
   } = {
      firstName: "Rubber",
      lastName: "Duck",
      email: "fdet.eu@gmail.com",
      username: "Duckie123",
      password: "BestDuck123.",
      confirmPassword: "BestDuck123.",
   };

   const regex = {
      emailRegex:
         /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
      usernameRegex: /^[a-zA-Z0-9_-]{3,}$/,
      passwordRegex:
         /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{5,}$/,
      firstNameRegex: /^[\p{L}'-]{2,}$/u,
      lastNameRegex: /^[\p{L}'-]{2,}(?: [\p{L}'-]+)*$/u,
   };

   async function onClick() {
      const inputs = Array.from(document.querySelectorAll<HTMLInputElement>("input"));

      const isValid = inputs.every((input) => checkType(user, input, false))

      if (!isValid) return console.log("not registering");

      console.log("registering");
   }

   function checkType(
      user: {
         firstName: string;
         lastName: string;
         email: string;
         username: string;
         password: string;
         confirmPassword: string;
      },
      e: HTMLInputElement | Event, 
      changeCol=true
   ) {
      let toCheck: HTMLInputElement;
      if (e instanceof HTMLInputElement) {
         toCheck = e;
      } else if (e instanceof Event) {
         toCheck = <HTMLInputElement>e.target;
      }

      switch (toCheck.name) {
         case "email":
            return check(toCheck, regex.emailRegex, changeCol);
            break;
         case "username":
            return check(toCheck, regex.usernameRegex, changeCol);
            break;
         case "password":
            return check(toCheck, regex.passwordRegex, changeCol);
            break;
         case "confirmPassword":
            const passwordConfirmRegex = `^${user.password}$`;
            return check(toCheck, new RegExp(passwordConfirmRegex), changeCol);
            break;
         case "firstName":
            return check(toCheck, regex.firstNameRegex, changeCol);
            break;
         case "lastName":
            return check(toCheck, regex.lastNameRegex, changeCol);
            break;
         default:
            break;
      }
   }

   function check(what: HTMLInputElement, how: RegExp, changeCol=true) {
      if (how.test(what.value)) {
         if (changeCol) { what.style.borderBottom = "2px solid green"; }
         return true;
      }
      if (changeCol) { what.style.borderBottom = "2px solid red" };
      return false
   }

   onMount(() => {
      const inputs = document.querySelectorAll<HTMLInputElement>("input");
      inputs.forEach((input) => {
         input.addEventListener("blur", (e) => {
            checkType(user, e);
         });
      });
   });

</script>

<section class="register-section">
   <LogRegSwitchBtn selectedButton="login" />

   <h1 class="no-margin">Register</h1>
   <div class="line">
      <label for="email">Email/Username</label>
      <input
         type="text"
         placeholder="Email/Username"
         bind:value={user.email}
         name="email"
      />
   </div>
   <div class="line">
      <label for="password">Password</label>
      <input
         type="password"
         placeholder="Password"
         bind:value={user.password}
         name="password"
      />
   </div>
   <section class="button-wrapper">
      <Button text="Register" whenClicked={onClick} />
   </section>
</section>

<style>
   .register-section {
      margin: 1em auto;

      width: 100%;
      max-width: 350px;

      background-color: var(--color-secondary);
      border-radius: 10px;

      margin-top: 8rem;
      padding: 0.8rem;

      white-space: nowrap;
   }

   .no-margin {
      margin: 0;
      padding: 0;
   }

   .line {
      width: 100%;

      display: flex;
      flex-direction: column;
      align-items: flex-start;

      margin-bottom: 0.2em;
   }

   .line > input {
      height: 1.6rem;
      width: 100%;

      border: none;
      border-bottom: 2px solid var(--color-tertiary);
      background-color: var(--color-primary-alpha);
      font-size: 1em;

      border-radius: 0.3em 0.3em 0 0;
   }

   .button-wrapper {
      margin-top: 0.6em;
   }
</style>
