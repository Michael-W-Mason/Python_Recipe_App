function deleteElement(ele){
    ele.parentNode.remove();
}

function addInput(ele, type){
    const HTMLdiv = document.createElement('div')
    HTMLdiv.className = 'p-2 input-group'

    const HTMLinput = document.createElement('input')
    // <input type="text" class="form-control" placeholder="Ingredient">
    HTMLinput.className = 'form-control input-group'
    HTMLinput.ariaLabel = ''
    HTMLinput.type = 'text'
    
    // <button class="btn btn-outline-secondary text-success-emphasis" type="button">Add Below</button>
    const HTMLAddButton = document.createElement('button')
    HTMLAddButton.className = 'btn btn-outline-secondary text-success-emphasis'
    HTMLAddButton.type = 'button'
    HTMLAddButton.innerText = 'Add Below'

    // <button onclick="deleteElement(this)" class="btn btn-outline-secondary text-danger-emphasis" type="button">Delete</button>
    const HTMLDelButton = document.createElement('button')
    HTMLDelButton.className = 'btn btn-outline-secondary text-danger-emphasis'
    HTMLDelButton.type = 'button'
    HTMLDelButton.innerText = 'Delete'
    HTMLDelButton.setAttribute('onclick', 'deleteElement(this)')

    if (type == 'ingredient'){
        HTMLinput.placeholder = 'Ingredient'
        HTMLinput.name = 'ingredient[]'
        HTMLAddButton.setAttribute('onclick', 'addInput(this, "instruction")')

    }
    if (type == 'instruction'){
        HTMLinput.placeholder = 'Instruction'
        HTMLinput.name = 'instruction[]'
        HTMLAddButton.setAttribute('onclick', 'addInput(this, "ingredient")')
    }

    HTMLdiv.appendChild(HTMLinput)
    HTMLdiv.appendChild(HTMLAddButton)
    HTMLdiv.appendChild(HTMLDelButton)
    
    ele.parentNode.insertAdjacentElement('afterend', HTMLdiv)
}

