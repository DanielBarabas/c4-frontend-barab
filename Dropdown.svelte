<!-- Dropdown.svelte -->
<script>
  export let options;
  export let selectedOption;
  export let handleChange;
</script>

<select value={selectedOption} on:change={handleChange}>
  {#each options as option}
    <option value={option}>{option}</option>
  {/each}
</select>
