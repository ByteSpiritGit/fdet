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
      firstName: "David",
      lastName: "Vrtulek",
      email: "fdet.eu@gmail.com",
      username: "fdet",
      password: "aA1.,",
      confirmPassword: "aA1.,",
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

   let buttonDisabled = false;

   async function onClick() {
      const inputs = document.querySelectorAll<HTMLInputElement>("input");
      inputs.forEach((input) => {
         console.log(input.name);
         checkType(user, input);
         buttonDisabled = false;
      });
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
      e: HTMLInputElement | Event
   ) {
      let toCheck: HTMLInputElement;
      if (e instanceof HTMLInputElement) {
         toCheck = e;
      } else if (e instanceof Event) {
         toCheck = <HTMLInputElement>e.target;
      }

      switch (toCheck.name) {
         case "email":
            check(toCheck, regex.emailRegex);
            break;
         case "username":
            check(toCheck, regex.usernameRegex);
            break;
         case "password":
            check(toCheck, regex.passwordRegex);
            break;
         case "confirmPassword":
            const passwordConfirmRegex = `^${user.password}$`;
            check(toCheck, new RegExp(passwordConfirmRegex));
            break;
         case "firstName":
            check(toCheck, regex.firstNameRegex);
            break;
         case "lastName":
            check(toCheck, regex.lastNameRegex);
            break;
         default:
            break;
      }
   }

   function check(what: HTMLInputElement, how: RegExp) {
      if (how.test(what.value)) {
         what.style.borderBottom = "2px solid green";

         return;
      }
      what.style.borderBottom = "2px solid red";
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
   <LogRegSwitchBtn selectedButton="register" />
   
   <h1 class="no-margin">Register</h1>
   <div class="line">
      <label for="firstName">First name</label>
      <input
         type="text"
         placeholder="First name"
         bind:value={user.firstName}
         name="firstName"
      />
   </div>
   <div class="line">
      <label for="lastName">Last name</label>
      <input
         type="text"
         placeholder="Last name"
         bind:value={user.lastName}
         name="lastName"
      />
   </div>
   <div class="line">
      <label for="email">Email</label>
      <input
         type="text"
         placeholder="Email"
         bind:value={user.email}
         name="email"
      />
   </div>
   <div class="line">
      <label for="username">Username</label>
      <input
         type="text"
         placeholder="Username"
         bind:value={user.username}
         name="username"
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
   <div class="line">
      <label for="confirmPassword">Confirm password</label>
      <input
         type="password"
         placeholder="Confirm password"
         bind:value={user.confirmPassword}
         name="confirmPassword"
      />
   </div>
   <section class="button-wrapper">
      <Button text="Register" whenClicked={onClick} disabled={buttonDisabled} />
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
