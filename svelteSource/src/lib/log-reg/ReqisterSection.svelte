<script lang="ts">
   import { onMount } from "svelte";
   import Button from "../Button.svelte";
   import LogRegSwitchBtn from "./LogReg_switch-btn.svelte";
   import NotificationBlock from "../notifications/NotificationBlock.svelte";
   import Notification from "../notifications/Notification.svelte";

   export let getCookie: (name: string) => string;

   let notificationBlock: HTMLDivElement;

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
      email: "duck.eu@gmail.com",
      username: "Duckie123",
      password: "BestDuck123.",
      // password: "BestDuck",
      confirmPassword: "BestDuck123.",
   };

   const regex = {
      emailRegex:
         /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
      usernameRegex: /^[a-zA-Z0-9_-]{3,}$/,
      passwordRegex:
         /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{5,}$/,
      firstNameRegex: /^[\p{L}'-]{2,}(?: [\p{L}'-]+)*$/u,
      lastNameRegex: /^[\p{L}'-]{2,}(?: [\p{L}'-]+)*$/u,
   };

   const notifs = {
      wrongPassword: {
         name: "Password must contain at least: ",
         description: `
            one digit (0-9)<br />
            one lowercase letter (a-z)<br />
            one uppercase letter (A-Z)<br />
            one special character (e.g. !@#$%^&*)<br />
            Be at least 5 characters long
         `,
         iconType: "Warning",
         duration: 5000
      },
      name: {
         name: "Something's wrong in the name: ",
         description: `
            The name should not contain any<br /> broken characters
         `,
         iconType: "Warning",
         duration: 5000
      },
      username: {
         name: "Username can contain: ",
         description: `
            letters, numbers, dashes and underscores<br />
            Be at least 3 characters long
         `,
         iconType: "Warning",
         duration: 5000
      },
      email: {
         name: "Email is not valid",
         description: `
            Please enter a valid email address<br />
            (e.g. john.doe@example.com)
         `,
         iconType: "Warning",
         duration: 5000
      },
      confirmPass: {
         name: "Passwords don't match",
         description: `
            Please make sure that the<br />passwords match
         `,
         iconType: "Warning",
         duration: 5000
      }
   }

   async function onClick() {
      const inputs = Array.from(document.querySelectorAll<HTMLInputElement>("input"));

      // const isValid = inputs.every((input) => checkType(user, input, true))
      let isValid = true;
      inputs.forEach((input) => {
         if (!checkType(user, input)) { 
            isValid = false;
         }
      });

      if (!isValid) {
         if ((<HTMLInputElement>document.querySelector("#firstname")).dataset.correct === "false") {
            new Notification({
               target: notificationBlock,
               props: notifs.name
            })
            console.log("nameWrong")
         }

         if ((<HTMLInputElement>document.querySelector("#lastname")).dataset.correct === "false") {
            new Notification({
               target: notificationBlock,
               props: notifs.name
            })
            console.log("nameWrong")
         }

         if ((<HTMLInputElement>document.querySelector("#username")).dataset.correct === "false") {
            new Notification({
               target: notificationBlock,
               props: notifs.username
            })
            console.log("usernameWrong")
         }

         if ((<HTMLInputElement>document.querySelector("#email")).dataset.correct === "false") {
            new Notification({
               target: notificationBlock,
               props: notifs.email
            })
            console.log("emailWrong")
         }

         
         if ((<HTMLInputElement>document.querySelector("#password")).dataset.correct === "false") {
            (<HTMLInputElement>document.querySelector("#password")).value = "";
            (<HTMLInputElement>document.querySelector("#confirmPassword")).value = "";
            new Notification({
               target: notificationBlock,
               props: notifs.wrongPassword
            })
            console.log("password wrong")
         }

         if ((<HTMLInputElement>document.querySelector("#confirmPassword")).dataset.correct === "false") {
            (<HTMLInputElement>document.querySelector("#confirmPassword")).value = "";
            new Notification({
               target: notificationBlock,
               props: notifs.confirmPass
            })
            console.log("confirmPassword wrong")
         }
         return console.log("not registering")
      };

      console.log("registering...");

      const csrftoken = getCookie("csrftoken");
      const url = "/registration"
      const request = new Request(url, {
         method: "POST",
         headers: { "X-CSRFToken": csrftoken },
         mode: "same-origin",
          body: JSON.stringify({
            first_name: user.firstName,
            last_name: user.lastName,
            email: user.email,
            username: user.username,
            password: user.password,
            password2: user.confirmPassword,
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
               iconType: "Warning",
               duration: 5000
            }
         })
         console.log("Server error")
         return response;
      }

      const final = await response.json();
      if (final["error_msg"] != undefined) {
         new Notification({
            target: notificationBlock,
            props: {
               name: "Something went wrong",
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

      console.log("success")
      console.log(final);

      window.location.href = "/";
      return final;
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
   <LogRegSwitchBtn selectedButton="register" />

   <h1 class="no-margin">Register</h1>
   <div class="line">
      <label for="firstName">First name</label>
      <input
         type="text"
         placeholder="First name"
         bind:value={user.firstName}
         name="firstName"
         id="firstname"
         data-correct="false"
      />
   </div>
   <div class="line">
      <label for="lastName">Last name</label>
      <input
         type="text"
         placeholder="Last name"
         bind:value={user.lastName}
         name="lastName"
         id="lastname"
         data-correct="false"
      />
   </div>
   <div class="line">
      <label for="email">Email</label>
      <input
         type="text"
         placeholder="Email"
         bind:value={user.email}
         name="email"
         id="email"
         data-correct="false"
      />
   </div>
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
   <div class="line">
      <label for="confirmPassword">Confirm password</label>
      <input
         type="password"
         placeholder="Confirm password"
         bind:value={user.confirmPassword}
         name="confirmPassword"
         id="confirmPassword"
         data-correct="false"
      />
   </div>
   <section class="button-wrapper">
      <Button text="Register" whenClicked={onClick} />
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
