const TierField = document.getElementById('id_tier') as HTMLSelectElement;
const Description = document.getElementById('description') as HTMLDivElement;
const DescriptionChildren = Array.prototype.slice.call(Description.children[0].children) as Array<HTMLDivElement>;
const SubmitButton = document.getElementById('input_id_submit') as HTMLInputElement;

// handle changes to the field
var handleChange = function() {
    var selected = TierField.options[TierField.selectedIndex].value;

    for(var i = 0; i < DescriptionChildren.length; i++) {
        DescriptionChildren[i].style.display = 'none';
    }
    const selectedTier = document.getElementById('description-' + selected) as HTMLDivElement;
    selectedTier.style.display = 'block';
    SubmitButton.value = (selected === 'st') ? window.tier_confirm_text : window.tier_next_text;
}

TierField.onchange = handleChange;
handleChange();
Description.style.display = 'block';
