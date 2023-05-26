<script lang="ts">
    export let icon: string;
    export let alt: string = undefined;
    export let url: string = undefined;
    export let color: string = "var(--color-text)";

    function maskSvg(icon: string, element) {
        element = element.parentElement;

        element.style.webkitMask = `url(${icon})`;
        element.style.mask = `url(${icon})`;
        element.style.webkitMaskSize = "100%";
        element.style.maskSize = "100%";
        element.style.webkitMaskPosition = "center";
        element.style.maskPosition = "center";
        element.style.webkitMaskRepeat = "no-repeat";
        element.style.maskRepeat = "no-repeat";

        element.style.display = "inline-block";

        element.style.backgroundColor = color;
    }
</script>

{#if url}
    <a class="mask" href="{url}" target="_blank" rel="noopener noreferrer">
        <img 
            src={icon} 
            alt={alt} 
            on:load={() => {maskSvg(icon, this.parent)}}
        />
    </a>
{:else}
    <div class="mask">
        <img 
            src={icon} 
            alt={alt}
            on:load={(e) => {maskSvg(icon, e.target)}}
        />
    </div>
{/if}

<style>
    img {
        display: none;
        
        width: 100%;
    }

    .mask {
        display: none;
        width: 100%;
        height: 100%;

        flex-shrink: 0;

        background-color: var(--color-text);
    }
</style>