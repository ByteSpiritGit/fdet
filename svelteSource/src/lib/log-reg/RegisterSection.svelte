<script lang="ts">
   import { onMount } from "svelte";
    import type { HtmlTag } from "svelte/internal";
    import Button from "../Button.svelte";

   let firstName: string;
   let lastName: string;
   let email: string;
   let username: string;
   let password: string;
   let confirmPassword: string;

   let user;

   const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
   const usernameRegex = /^[a-zA-Z0-9_-]{3,}$/;
   const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{5,}$/;
   const firstNameRegex = /^[\p{L}'-]{2,}$/u;
   const lastNameRegex = /^[\p{L}'-]{2,}(?: [\p{L}'-]+)*$/u;

   $: user = {
      firstName: firstName,
      lastName: lastName,
      email: email,
      username: username,
      password: password,
      confirmPassword: confirmPassword
   }
      
   function register(inputs) {
      inputs.forEach(input => {
         console.log(input.name)
         checkType(input)
      });
      console.log(user)
   }

   function checkType(e: HTMLInputElement | Event) {
      let toCheck: HTMLInputElement;
      if (e instanceof HTMLInputElement) {
         toCheck = e;
      }
      else if (e instanceof Event) {
       toCheck = (<HTMLInputElement>e.target)
      }

      switch (toCheck.name) {
         case "email":
            check(toCheck, emailRegex)
            break;
         case "username":
            check(toCheck, usernameRegex)
            break;
         case "password":
            check(toCheck, passwordRegex)
            break;
         case "confirmPassword":
            const passwordConfirmRegex = `^${password}$`;
            check(toCheck, new RegExp(passwordConfirmRegex))
            break;
         case "firstName":
            check(toCheck, firstNameRegex)
            break;
         case "lastName":
            check(toCheck, lastNameRegex)
            break;
         default:
            break;
      }
   }

   onMount(() => {
      const inputs = document.querySelectorAll<HTMLInputElement>("input");
      inputs.forEach(input => {
         input.addEventListener("blur", (e) => {
            checkType(e)
         })
      })

      document.addEventListener("keydown", (e) => {
         if (e.key === "Enter") {
            register(inputs)     
         }
      })
   })

   function check(what:HTMLInputElement, how:RegExp) {
      if (how.test(what.value)) {
         what.style.borderBottom = "2px solid green";

         return;
      }
      what.style.borderBottom = "2px solid red";
   }
</script>

<section class="registration">
   <h1>Register</h1>
   <div class="line">
      <label for="firstName">First name</label>
      <input type="text" placeholder="First name" bind:value={firstName} name="firstName" />
   </div>
   <div class="line">
      <label for="lastName">Last name</label>
      <input type="text" placeholder="Last name" bind:value={lastName} name="lastName" />
   </div>
   <div class="line">
      <label for="email">Email</label>
      <input type="text" placeholder="Email" bind:value={email} name="email" />
   </div>
   <div class="line">
      <label for="username">Username</label>
      <input type="text" placeholder="Username" bind:value={username} name="username" />
   </div>
   <div class="line">
      <label for="password">Password</label>
      <input type="password" placeholder="Password" bind:value={password} name="password" />
   </div>
   <div class="line">
      <label for="confirmPassword">Confirm password</label>
      <input type="password" placeholder="Confirm password" bind:value={confirmPassword} name="confirmPassword" />
   </div>
   <button on:click={register} disabled>Register</button>
</section>

<style>
   .registration {
      display: flex;
      flex-direction: column;
      align-items: center;

      width: fit-content;

      margin: 0 auto;
      margin-top: 5em;
      padding: 1.25rem;

      background-color: var(--color-secondary);
      border-radius: 10px;

   }

   .registration > h1 {
      margin: 0;
      padding: 0;
   }

   .line {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

      width: 100%;
   }

   label {
      text-align: left;
      width: 100%;

      font-size: 1rem;
   }

   .line > input {
      /* modern input */
      width: 300px;
      height: 2rem;

      padding: 0.5rem;
      border: 1px solid var(--color-primary);
      border-radius: 0.25rem;
      font-size: 1rem;
      font-family: inherit;
      box-shadow: inset 1px 1px 3px var(--color-primary);
      transition: border-color 0.1s ease-in-out, box-shadow 0.2s ease-in-out;
   }

   .line > input:focus {
      outline: none;
      border-color: var(--color-tertiary);
   }

   button {
      width: 300px;
      height: 2rem;

      margin-top: 1rem;

      border: none;
      border-radius: 0.25rem;
      background-color: var(--color-primary);
      color: var(--color-text);
      font-size: 1rem;
      font-family: inherit;
      box-shadow: 1px 1px 3px var(--color-primary);
      transition: background-color 0.1s ease-in-out, box-shadow 0.2s ease-in-out;
   }

   button:hover {
      background-color: var(--color-tertiary);
      box-shadow: 1px 1px 3px var(--color-tertiary);
   }

   button:active {
      background-color: var(--color-secondary);
      box-shadow: 1px 1px 3px var(--color-secondary);
   }
</style>