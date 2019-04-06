window.onload = function() {
    // fetch all the elements on the page
    var TierField = document.getElementById('id_tier');
    var Description = document.getElementById('description');
    var DescriptionChildren = Array.prototype.slice.call(Description.children[0].children);
    var StarterReasonField = document.getElementById('div_id_starterReason');
    
    // flip the order of description and children
    Description.parentNode.removeChild(Description);
    StarterReasonField.parentNode.insertBefore(Description, StarterReasonField);

    // handle changes to the field
    var handleChange = function() {
        var selected = TierField.options[TierField.selectedIndex].value;

        for(var i = 0; i < DescriptionChildren.length; i++) {
            DescriptionChildren[i].style.display = 'none';
        }

        document.getElementById('description-' + selected).style.display = 'block';

        if (selected === 'st') {
            StarterReasonField.style.display = 'block';
        } else {
            StarterReasonField.style.display = 'none';
        }
    }

    TierField.onchange = handleChange;
    handleChange();
    Description.style.display = 'block';
}