<script lang="ts">
   import Notification from "./notifications/Notification.svelte";
   import NotificationBlock from "./notifications/NotificationBlock.svelte";

   let notificationBlock: HTMLDivElement;

    const logedin: boolean = localStorage.getItem("logged") === "true";
    const username: string = localStorage.getItem("username");
    if (logedin && username === null || username === undefined || username === "") {
        authenticate();
    }

   function getCsrfToken() {
      var xhr = new XMLHttpRequest();
      // Set up a callback function to handle the response
      xhr.onreadystatechange = function () {
         if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
               try {
                  document.cookie =
                     "csrftoken=" +
                     encodeURIComponent(
                        JSON.parse(xhr.responseText).csrf_token
                     ) +
                     "; path=/";
               } catch (error) {
                  console.log(error);
               }
            } else {
               console.log("Request failed");
            }
         }
      };

      xhr.open("GET", "/csrf_view");
      xhr.send();
   }

   function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
         const cookies = document.cookie.split(";");
         for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
               cookieValue = decodeURIComponent(
                  cookie.substring(name.length + 1)
               );
               break;
            }
         }
      }
      return cookieValue;
   }

   async function logout() {
      getCsrfToken();
        localStorage.removeItem("logged");

      const csrftoken = getCookie("csrftoken");

      const url = "/logout"
      const request = new Request(url, {
         method: "POST",
         mode: "same-origin",
         headers: { "X-CSRFToken": csrftoken },
      });

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

      localStorage.removeItem("logged");
      localStorage.removeItem("username");
      window.location.href = "/";
   }

    async function authenticate() {
        const csrftoken = getCookie("csrftoken");
        
        const request = new Request("/authentication", {
            method: "POST",
            mode: "same-origin",
            headers: { "X-CSRFToken": csrftoken },
        });

        const response = await fetch(request);
        
        switch (response.status) {
            case 200:
                localStorage.setItem("logged", "true");
                localStorage.setItem("username", (await (response.json())).username);
                break;
            case 401:
                localStorage.removeItem("logged");
                window.location.href = "/";
                break;
            default:
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
                break;
        }

    }
</script>

<nav class="navbar">
   <section class="menu-section">
      <a href="/">Home</a>
      <a href="/">About us</a>
      <a href="/">Learn</a>
      <a href="https://github.com/fdet/fDet">Github</a>
   </section>
   <section class="sides-section">
      <section class="logo-section">
         <h3 class="no-margin">fDet</h3>
         <p class="no-margin">by ByteSpirit</p>
      </section>
      {#if logedin}
         <section class="underneath">
            <a href="/" class="no-margin">User: {localStorage.getItem("username")}</a>
            <a on:click={logout} href="#logout" class="no-margin"><b>Logout</b></a>
         </section>
      {:else}
         <section class="profile-section">
            <a href="/users/login" class="no-margin">Login</a>
            <a href="/users/register" class="no-margin"><b>Register</b></a>
         </section>
      {/if}
   </section>
</nav>

<NotificationBlock bind:theComponent={notificationBlock} notificationNumber={1} />

<style>
   .underneath {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: flex-start;
   }

   .underneath > a {
      text-align: left;
      justify-content: flex-start;

      padding-left: 0.35em;
   }

   .logo-section {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: center;

      padding: 0.5em;
   }

   .profile-section > a:hover, .underneath > a:hover{
      text-shadow: 0px 0px 1px #ffffffce, 0px 0px 10px #cccccc77;
   }

   .profile-section {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-evenly;

      padding: 0.5em;
   }

   .no-margin {
      margin: 0;
      padding: 0;

      line-height: 1em;
   }

   a {
      color: var(--color-text);
      text-decoration: none;

      width: 100%;
      height: 100%;

      display: flex;
      align-items: center;
      justify-content: center;

      white-space: nowrap;

      padding: 0 0.5em;
      border: none;
   }

   a:focus {
      border: none;
      outline: 2px solid var(--color-text);
      outline-offset: -2px;
   }

   .navbar {
      position: fixed;
      top: 0;

      z-index: 200;

      width: 100%;
      height: 3.5rem;

      font-size: 1.2em;

      background-color: var(--color-primary);

      box-shadow: 0 0 10px 1px var(--color-primary);
   }
   
   .sides-section {
      position: relative;
      z-index: 250;
      top: -3.5rem;

      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;

      width: 100%;
      height: 3.5rem;
   }

   .sides-section > section {
      width: 150px;
      background-color: var(--color-secondary);
      height: 100%;

      border: none;
   }

   .sides-section > section:first-child {
      border-radius: 0 0 10px 0;
   }

   .sides-section > section:last-child {
      border-radius: 0 0 0 10px;
   }

   .menu-section {
      position: relative;
      z-index: 500;

      width: 100%;
      height: 3.5rem;

      border-radius: 0 0 10px 10px;
      width: fit-content;

      margin: 0 auto;
      left: 0;
      right: 0;


      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-evenly;

      overflow: hidden;

      background-color: var(--color-secondary);
   }

   .menu-section > a:hover {
      background-color: var(--color-tertiary);
   }

   @media (max-width: 680px) {
      .navbar {
         height: 7rem;
      }

      .sides-section {
         top: 0;
      }

      .sides-section > section {
         width: 100%;
         
         border-width: 2px 0 0 0;
         border-color: var(--color-primary);
         border-style: solid;
      }

      .sides-section > section:first-child {
         border-radius: 0 0 0 0;
         box-shadow: none;

         border-width: 2px 2px 0 0;
      }

      .sides-section > section:last-child {
         border-radius: 0 0 0 0;
         box-shadow: none;
      }
      
      .menu-section {
         border-radius: 0 0 0 0;

         width: 100%;
      }
   }
</style>