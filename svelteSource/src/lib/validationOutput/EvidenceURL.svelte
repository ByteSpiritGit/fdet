<script lang="ts">
    export let url: string;
    export let evidence: string;

    const words = evidence.split(".");
    let firstPiece:string = words[0].split(",")[0];
    let lastPiece = words[words.length - 1] === "" ? words[words.length - 2] : words[words.length - 1];  
    lastPiece = lastPiece.split(",").slice(-1)[0];
</script>

{#if evidence.length < 4}
    <a class="evidence-url" href={`${url}#${evidence}`}>
        {url.split("/").slice(-1)}...
    </a>
{:else}
    <a class="evidence-url" href={`${url}#:~:text=${firstPiece},${lastPiece}`}>
        wikipedia/{url.split("/").slice(-1)}...
    </a>
{/if}

<style>
    .evidence-url {
        background-color: var(--color-tertiary-alpha);
        border-radius: 0.35em;
        color: var(--color-text);
        padding: 0.1em;
        text-decoration: none;

        transition: 0.4s;

        margin-right: 0.5em;
    }

    .evidence-url:hover {
        background-color: var(--color-tertiary);
        text-decoration: dotted underline;
    }
</style>