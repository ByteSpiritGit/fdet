<script lang="ts">
   import { onMount } from "svelte";
   import Button from "../Button.svelte";
   import LogRegSwitchBtn from "./LogReg_switch-btn.svelte";
   import NotificationBlock from "../notifications/NotificationBlock.svelte";
   import Notification from "../notifications/Notification.svelte";

   export let getCookie: (name: string) => string;

   let notificationBlock: HTMLDivElement;

   let user: {
      username: string,
      password: string
   } 
   = {
      username: "",
      password: ""
   };

   const regex = {
      usernameRegex: /^[a-zA-Z0-9_-]{3,}$/,
      passwordRegex: /.{5,}/
   };

   const notifs = {
      wrongPassword: {
         name: "Wrong password",
         description: `
            Password is incorrect.
         `,
         iconType: "Warning",
         duration: 5000
      },
      wrongUsername: {
         name: "Username format wrong: ",
         description: `
            Must be at least 3 characters long
         `,
         iconType: "Warning",
         duration: 5000
      }
   }

   async function onClick() {
      const inputs = Array.from(document.querySelectorAll<HTMLInputElement>("input"));

      // Check all inputs
      let isValid = true;
      inputs.forEach((input) => {
         if (!checkType(user, input)) { 
            isValid = false;
         }
      });

      if (!isValid) {
         if ((<HTMLInputElement>document.querySelector("#username")).dataset.correct === "false") {
            new Notification({
               target: notificationBlock,
               props: notifs.wrongUsername
            })
            console.log("Wrong username format")
         }
         else if ((<HTMLInputElement>document.querySelector("#password")).dataset.correct === "false") {
            (<HTMLInputElement>document.querySelector("#password")).value = "";
            new Notification({
               target: notificationBlock,
               props: notifs.wrongPassword
            })
            console.log("Wrong password format")
         }
         return console.log("not logging in")
      };

      console.log("logging in...");

      const csrftoken = getCookie("csrftoken");
      const url = "/login"
      const request = new Request(url, {
         method: "POST",
         headers: { "X-CSRFToken": csrftoken },
         mode: "same-origin",
         body: JSON.stringify({
            username: user.username,
            password: user.password
         }),
      });

      // Handle errors in the response
      const response = await fetch(request);
      if (response.status != 200) {
         new Notification({
            target: notificationBlock,
            props: {
               name: "Something went wrong",
               description: `Error ${response.status}: ${response.statusText}`,
               iconType: response.status === 404 ? "ehh" : "Warning",
               duration: 5000
            }
         })
         console.log("Server error")
         return response;
      }

      // Handle errors about the user
      const final = await response.json();
      if (final["error_msg"] != undefined) {
         new Notification({
            target: notificationBlock,
            props: {
               name: "Invalid credentials",
               description: `Error ${final["status"]}: ${final["error_msg"]}`,
               iconType: "Warning",
               duration: 5000
            }
         })
         console.log("User error")
         return final;
      }

      localStorage.setItem("logged", "true");
      localStorage.setItem("username", user.username);

      console.log("success");

      window.location.href = "/";
      return final;
   }

   function checkType(
      user: {
         username: string,
         password: string
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
         case "username":
            return check(toCheck, regex.usernameRegex, changeCol);
         case "password":
            return check(toCheck, regex.passwordRegex, changeCol);
         default:
            break;
      }
   }

   function check(what: HTMLInputElement, how: RegExp, changeCol=true) {
      if (how.test(what.value)) {
         if (changeCol) { what.style.borderBottom = "2px solid green"; }
         what.setAttribute("data-correct", "true")
         return true;
      }
      if (changeCol) { what.style.borderBottom = "2px solid red" };
      what.setAttribute("data-correct", "false")
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

   <h1 class="no-margin">Login</h1>
   <div class="line">
      <label for="username">Username</label>
      <input
         type="text"
         placeholder="Username"
         bind:value={user.username}
         name="username"
         id="username"
         data-correct="false"
      />
   </div>
   <div class="line">
      <label for="password">Password</label>
      <input
         type="password"
         placeholder="Password"
         bind:value={user.password}
         name="password"
         id="password"
         data-correct="false"
      />
   </div>
   <section class="button-wrapper">
      <Button text="Login" whenClicked={onClick} />
   </section>
</section>

<NotificationBlock bind:theComponent={notificationBlock} notificationNumber={3} />

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
