<script lang="ts">
   import { onMount } from "svelte";

   import ClaimSection from "./ClaimSection.svelte";
   import InputSection from "../InputSection.svelte";
   import Notification from "../notifications/Notification.svelte";
   import NotificationBlock from "../notifications/NotificationBlock.svelte";


   export let getCsrfToken: () => void;
   export let getCookie: (name: string) => string;
   export let toEvaluate: string;

   let chat;

   let textarea: HTMLTextAreaElement;
   let notifs;

   onMount(() => {
      evaluate(toEvaluate).then((response) => {
         console.log(response);
         new ClaimSection({
            target: chat,
            props: {
               claims: response,
               id_offset: 0,
            },
         });
      });
      chat.scrollTop = chat.scrollHeight - chat.clientHeight;
   });

   async function evaluate(text: string) {
      const csrftoken = getCookie("csrftoken");
      let url = `/rag_evaluation?text=${text}`;

      const request = new Request(url, {
         method: "POST",
         headers: { "X-CSRFToken": csrftoken },
         mode: "same-origin",
      });

      try {
         const response = (await (await fetch(request)).json()).validated;
         const urlParams = new URLSearchParams(window.location.search);
         urlParams.delete("text");
         window.history.replaceState(
            {},
            "",
            `${window.location.pathname}?${urlParams}`
         );
         return response;
      } catch (error) {
         return [
            {
               claim: "Vaccines do not cause autism",
               evidence:
                  "Numerous studies have shown that there is no link between vaccines and autism. The original study that suggested a link has been discredited and retracted by the journal that published it.",
               label: "Supports",
               refutes: 0.1,
               supports: 0.9,
               nei: 0,
               justify:
                  "The overwhelming majority of scientific evidence shows that there is no link between vaccines and autism. This includes large-scale studies involving millions of children, as well as reviews by independent expert panels. The original study that suggested a link has been widely discredited and retracted by the journal that published it.",
            },
            {
               claim: "Vaccines are not effective",
               evidence:
                  "Vaccines have been proven to be highly effective at preventing infectious diseases. For example, the measles vaccine has been estimated to prevent 13.3 million deaths worldwide between 2000 and 2018.",
               label: "Refutes",
               refutes: 0.8,
               supports: 0.1,
               nei: 0.1,
               justify:
                  "Numerous studies have shown that vaccines are highly effective at preventing infectious diseases. For example, the measles vaccine has been estimated to prevent 13.3 million deaths worldwide between 2000 and 2018. Vaccines have also been instrumental in eradicating diseases like smallpox and nearly eradicating others like polio.",
            },
            {
               claim: "Vaccines are dangerous and can cause serious side effects",
               evidence:
                  "Vaccines are rigorously tested and monitored for safety. Serious side effects are rare and typically outweighed by the benefits of vaccination in preventing serious illness and death.",
               label: "Refutes",
               refutes: 0.7,
               supports: 0.15,
               nei: 0.15,
               justify:
                  "Vaccines are one of the most rigorously tested and monitored medical interventions. The vast majority of people who receive vaccines experience only mild side effects, such as soreness at the injection site or a low-grade fever. Serious side effects are rare and typically outweighed by the benefits of vaccination in preventing serious illness and death.",
            },
            {
               claim: "Vaccines are not necessary because diseases are no longer a threat",
               evidence:
                  "Vaccine-preventable diseases are still a threat in many parts of the world, and outbreaks can occur when vaccination rates drop. For example, there have been recent outbreaks of measles in several countries including the United States and Europe.",
               label: "Refutes",
               refutes: 0.7,
               supports: 0.2,
               nei: 0.1,
               justify:
                  "Vaccine-preventable diseases are still a threat in many parts of the world, and outbreaks can occur when vaccination rates drop. For example, there have been recent outbreaks of measles in several countries including the United States and Europe. Vaccines have been instrumental in reducing the incidence of many serious infectious diseases and have saved countless lives.",
            },
            {
               claim: "Vaccines can cause the disease they are intended to prevent",
               evidence:
                  "Vaccines do not contain live viruses or bacteria for the diseases they are intended to prevent, so they cannot cause the disease. Some vaccines do contain weakened or inactivated forms of the virus or bacteria, but these are not capable of causing the disease.",
               label: "Supports",
               refutes: 0.05,
               supports: 0.95,
               nei: 0,
               justify:
                  "This claim is a common misconception about vaccines. In reality, vaccines do not contain live viruses or bacteria for the diseases they are intended to prevent, so they cannot cause the disease. Some vaccines do contain weakened or inactivated forms of the virus or bacteria, but these are not capable of causing the disease. The side effects of vaccines are usually mild and temporary, such as soreness or redness at the injection site or a low-grade fever.",
            },
            {
               claim: "Vaccines are only for children",
               evidence:
                  "While childhood vaccination is important, vaccines are also recommended and available for adults. Some vaccines, such as the flu vaccine, are recommended for all adults, while others are recommended for specific groups based on age, occupation, travel plans, or other factors.",
               label: "Supports",
               refutes: 0.2,
               supports: 0.7,
               nei: 0.1,
               justify:
                  "While childhood vaccination is important, vaccines are also recommended and available for adults. Some vaccines, such as the flu vaccine, are recommended for all adults, while others are recommended for specific groups based on age, occupation, travel plans, or other factors. Vaccination is an important part of protecting public health and preventing the spread of infectious diseases.",
            },
            {
               claim: "Natural immunity is better than vaccine-induced immunity",
               evidence:
                  "While natural immunity can provide protection against some diseases, it is not always as effective or long-lasting as vaccine-induced immunity. Additionally, getting vaccinated can prevent serious complications or death from vaccine-preventable diseases.",
               label: "Refutes",
               refutes: 0.6,
               supports: 0.1,
               nei: 0.3,
               justify:
                  "While natural immunity can provide protection against some diseases, it is not always as effective or long-lasting as vaccine-induced immunity. Additionally, getting vaccinated can prevent serious complications or death from vaccine-preventable diseases. It is important to follow the recommended vaccination schedule to ensure adequate protection against infectious diseases.",
            },
            {
               claim: "Vaccines contain dangerous chemicals",
               evidence:
                  "Vaccines do contain some chemicals, but these are used to enhance the effectiveness and safety of the vaccine. The chemicals in vaccines are carefully evaluated for safety and are used in very small amounts.",
               label: "Supports",
               refutes: 0.15,
               supports: 0.6,
               nei: 0.25,
               justify:
                  "Vaccines do contain some chemicals, but these are used to enhance the effectiveness and safety of the vaccine. The chemicals in vaccines are carefully evaluated for safety and are used in very small amounts. In fact, many of the chemicals found in vaccines are also present in everyday foods and consumer products.",
            },
            {
               claim: "Vaccines are a plot by pharmaceutical companies to make money",
               evidence:
                  "Vaccines are developed and recommended by independent organizations, such as the Centers for Disease Control and Prevention and the World Health Organization. While pharmaceutical companies do produce vaccines, they are subject to strict regulation and are required to provide evidence of safety and effectiveness before they can be approved for use.",
               label: "Refutes",
               refutes: 0.8,
               supports: 0.1,
               nei: 0.1,
               justify:
                  "Vaccines are developed and recommended by independent organizations, such as the Centers for Disease Control and Prevention and the World Health Organization. While pharmaceutical companies do produce vaccines, they are subject to strict regulation and are required to provide evidence of safety and effectiveness before they can be approved for use. Vaccination is an important part of protecting public health and preventing the spread of infectious diseases.",
            },
         ];
      }
   }

   let whenClk = () => {
      const isthereTextRegex = /\S/;
      if (!isthereTextRegex.test(textarea.value)) {
         const notification = new Notification({
            target: notifs,
            props: {
               name: "Text missing",
               description: "There is nothing to evaluate",
               iconType: "Warning",
               duration: 5000,
            },
         });
         return;
      }
      
      console.log("Claim block- whenClk");
      evaluate(textarea.value).then((res) => {
         console.log(res);
         textarea.value = "";
         new ClaimSection({
            target: chat,
            props: {
               claims: res,
               id_offset: document.querySelectorAll(".claim-section").length,
            },
         });
      chat.scrollTop = chat.scrollHeight - chat.clientHeight;
      });
   };
</script>

<output class="chat" bind:this={chat} />

<InputSection bind:textarea buttonDisabled={false} {whenClk} />

<NotificationBlock bind:theComponent={notifs} notificationNumber={1} />

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
