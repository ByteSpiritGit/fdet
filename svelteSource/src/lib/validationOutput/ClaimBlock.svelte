<script lang="ts">
   import { onMount } from "svelte";

   import ClaimSection from "./ClaimSection.svelte";
   import InputSection from "../InputSection.svelte";
   import Notification from "../notifications/Notification.svelte";
   import NotificationBlock from "../notifications/NotificationBlock.svelte";
   import Loading from "../Loading.svelte";

   // export let getCsrfToken: () => void;
   export let getCookie: (name: string) => string;

   let chat: HTMLOutputElement;

   let textarea: HTMLTextAreaElement;
   let notificationBlock: HTMLDivElement;
   let disabled = false;

   onMount(() => {
      whenClk();
   });

   // requests from server and processes the data
   async function evaluate(text: string) {
      // when there was an enter, the '.' had letters next to it and the sentence splitter didn't work
      let urlText = "";
      text.split("\n").forEach(claim => {
         urlText += claim + " ";
      });
      text = urlText

      // creates loading and disables the button
      const loading = new Loading({
         target: chat,
         props: {
            id: document
               .getElementsByClassName("claim-section")
               .length.toString(),
         },
      });
      disabled = true;

      const csrftoken = getCookie("csrftoken");
      let url = `/rag_evaluation?text=${text}`;
      const request = new Request(url, {
         method: "POST",
         headers: { "X-CSRFToken": csrftoken },
         mode: "same-origin",
      });

      // Handle errors in the response
      const response = await fetch(request);
      if (response.status > 299) {
         console.log(response)
         return [
            {
               claim: response.statusText,
               evidence: response.statusText,
               label: "Error " + response.status,
               refutes: 0,
               nei: 0,
               supports: 0,
               justify: "OK? " + response.ok,
            },
         ];
      }

      const final: Array<{
         claim: string,
         evidence: string,
         label: string,
         refutes: number,
         supports: number,
         nei: number,
         justify: string,
      }> = (await (response.json())).validated;
      return final;
   }

   function whenClk(fromInput = false) {
      const isthereTextRegex = /\S/;
      const urlParams = new URLSearchParams(window.location.search);

      // Check if there is data in the input, URL or session storage, otherwise show a warning
      if (fromInput && !isthereTextRegex.test(textarea.value) || !urlParams.get("text") && !window.sessionStorage.getItem("evalued")) {
         const notification = new Notification({
            target: notificationBlock,
            props: {
               name: "Text missing",
               description: "There is nothing to evaluate",
               iconType: "Warning",
               duration: 5000,
            },
         });
         return;
      }

      // If there is data in session storage and not anywhere else, use that
      if (!isthereTextRegex.test(textarea.value) && !urlParams.get("text") && window.sessionStorage.getItem("evalued")) {
         console.log("from storage")
         const fromStorage = JSON.parse(window.sessionStorage.getItem("evalued"))
         new ClaimSection({
            target: chat,
            props: {
               claims: fromStorage,
               id_offset: document.getElementsByClassName("claim-section").length,
            },
         });
         chat.scrollTop = chat.scrollHeight - chat.clientHeight;
         return;
      }

      // URL has priority over everything
      let text = textarea.value;
      let fromWhere = "from input"
      if (urlParams.get("text")) {
         fromWhere = "from url"
         text = urlParams.get("text");

         urlParams.delete("text");
         window.history.replaceState(
            {},
            "",
            `${window.location.pathname}?${urlParams}`
         );
      }

      console.log(fromWhere)
      // request it
      evaluate(text).then((res) => {
         console.log(res);
         textarea.value = "";

         // remove loading
         document.getElementById(`${document.getElementsByClassName("claim-section").length}l`).remove();
         disabled = false;

         new ClaimSection({
            target: chat,
            props: {
               claims: res,
               id_offset:
                  document.getElementsByClassName("claim-section").length,
            },
         });
         chat.scrollTop = chat.scrollHeight - chat.clientHeight;

         window.sessionStorage.setItem("evalued", JSON.stringify(res));
      });
   };
</script>

<output class="chat" bind:this={chat} />

<InputSection bind:textarea buttonDisabled={disabled} whenClk={whenClk} />

<NotificationBlock bind:theComponent={notificationBlock} notificationNumber={1} />

<style>
   .chat {
      position: absolute;
      top: 3.5rem;
      bottom: 10rem;

      width: 100%;
      max-width: 1100px;

      overflow-y: auto;
      overflow-x: hidden;

      padding: 0.5rem;
      padding-bottom: 0;
   }

   @media (max-width: 680px) {
      .chat {
         top: 7rem;
      }
   }
</style>
