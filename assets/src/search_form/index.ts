(function(){
        // the thing to add to the search
        const searchInput = document.getElementById('searchInput') as HTMLInputElement;
        const advancedTable = document.getElementById('advancedFieldTable') as HTMLTableElement;
        const tableBody = advancedTable.children[0] as HTMLTableSectionElement;

        // select the advanced table
        Array.prototype.forEach.call(tableBody.children, function(advancedField){
            const selector = advancedField.children[0].getAttribute('data-selector');
            const select = advancedField.children[1].children[0].children[0];

            const button = document.createElement('button');
            advancedField.children[1].children[0].appendChild(button);
            button.setAttribute('type', 'button');
            button.setAttribute('id', 'aft_id_button_' + selector);
            button.className = 'uk-button uk-button-default';
            button.innerHTML = '+';

            button.addEventListener('click', function(evt){
                evt.stopImmediatePropagation();
                var value = select.options[select.selectedIndex].value;
                searchInput.value = searchInput.value + ' ' + selector + ': ' + value;
                return false;
            }, false);
        });

        // on submitting the form, remove all the extra fields in the table
        searchInput.form!.addEventListener("submit", function(){
            advancedTable.parentElement!.removeChild(advancedTable);
        }, false);
    })();