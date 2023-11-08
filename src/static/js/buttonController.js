function deleteElement(ele){
    ele.parentNode.remove();
}

function addIngredient(){
    const HTMLdiv = document.createElement('div')
    HTMLdiv.className = 'ingredient'

    const HTMLinput = document.createElement('input')
    HTMLinput.type = 'text'
    HTMLinput.name = 'ingredient[]'
    
    const HTMLbutton = document.createElement('button')
    HTMLbutton.setAttribute('onclick', 'deleteElement(this)')
    HTMLbutton.type = 'button'
    HTMLbutton.innerText = 'Delete'

    HTMLdiv.appendChild(HTMLinput)
    HTMLdiv.appendChild(HTMLbutton)
    
    document.getElementById('ingredients').appendChild(HTMLdiv)
}

function addInstruction(){
    const HTMLdiv = document.createElement('div')
    HTMLdiv.className = 'instruction'

    const HTMLinput = document.createElement('input')
    HTMLinput.type = 'text'
    HTMLinput.name = 'instruction[]'
    
    const HTMLbutton = document.createElement('button')
    HTMLbutton.setAttribute('onclick', 'deleteElement(this)')
    HTMLbutton.type = 'button'
    HTMLbutton.innerText = 'Delete'

    HTMLdiv.appendChild(HTMLinput)
    HTMLdiv.appendChild(HTMLbutton)
    
    document.getElementById('instructions').appendChild(HTMLdiv)
}

