<!-- App.svelte -->
<script>
  import Dropdown from './Dropdown.svelte';

  let categoryOptions = ["Sex & Nudity", "Violence & Gore", "Profanity", "Alcohol, Drugs & Smoking", "Frightening & Intense Scenes"];
  let severityOptions = ["Severe", "Moderate", "Mild"];

  let selectedCategory;
  let selectedSeverity;

  function handleCategoryChange(event) {
    selectedCategory = event.target.value;
  }

  function handleSeverityChange(event) {
    selectedSeverity = event.target.value;
  }
</script>

<h1>Select Category:</h1>
<Dropdown options={categoryOptions} selectedOption={selectedCategory} handleChange={handleCategoryChange} />

<h1>Select Severity:</h1>
<Dropdown options={severityOptions} selectedOption={selectedSeverity} handleChange={handleSeverityChange} />
