var tier_change_init = function(continue_text, confirm_text) {
    // fetch all the elements on the page
    var TierField = document.getElementById('id_tier');
    var Description = document.getElementById('description');
    var DescriptionChildren = Array.prototype.slice.call(Description.children[0].children);
    var SubmitButton = document.getElementById('input_id_submit');

    // handle changes to the field
    var handleChange = function() {
        var selected = TierField.options[TierField.selectedIndex].value;

        for(var i = 0; i < DescriptionChildren.length; i++) {
            DescriptionChildren[i].style.display = 'none';
        }

        document.getElementById('description-' + selected).style.display = 'block';
        SubmitButton.value = (selected === 'st') ? confirm_text : continue_text;
    }

    TierField.onchange = handleChange;
    handleChange();
    Description.style.display = 'block';
}