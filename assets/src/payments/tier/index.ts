// TOOD: We should migrate this to vue and do local inference
import {memberCategory, MemberTier, getAllowedTiers, MemberTierTitles, MemberTierDescriptions} from "../../base/utils/membership";

// load a lot of html elements
const TierField = document.getElementById('id_tier') as HTMLSelectElement;
const Description = document.getElementById('description') as HTMLDivElement;
const DescriptionChildren = Array.prototype.slice.call(Description.children[0].children) as Array<HTMLDivElement>;
const SubmitButton = document.getElementById('input_id_submit') as HTMLInputElement;

// iterate over the <divs> and add the description
getAllowedTiers().forEach((tier) => {
    const element = document.getElementById(`description-${tier}`) as HTMLDivElement;
    
    // create the title
    const titleP = document.createElement('p');
    titleP.innerHTML = MemberTierTitles[tier];
    element.appendChild(titleP);

    // create the description
    const descriptionP = document.createElement('p');
    descriptionP.innerHTML = MemberTierDescriptions[tier];
    element.appendChild(descriptionP);
})


// handle changes to the tier field
function handleChange() {
    var selected = TierField.options[TierField.selectedIndex].value;

    for(var i = 0; i < DescriptionChildren.length; i++) {
        DescriptionChildren[i].style.display = 'none';
    }
    const selectedTier = document.getElementById(`description-${selected}`) as HTMLDivElement;
    selectedTier.style.display = 'block';
    SubmitButton.value = (selected === 'st') ? window.tier_confirm_text : window.tier_next_text;
}
TierField.onchange = handleChange;
handleChange();

// and enable the page
Description.style.display = 'block';
SubmitButton.removeAttribute('disabled');
